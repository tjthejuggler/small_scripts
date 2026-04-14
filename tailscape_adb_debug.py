#!/usr/bin/env python3
"""
ADB over Tailscale - connect to your phone via ADB on port 5555.

If port 5555 isn't listening (e.g. after a phone reboot), the script will:
  1. Scan for the Wireless Debugging random port via nmap
  2. Connect on that port
  3. Run 'adb tcpip 5555' to re-enable port 5555 for future use
  4. Reconnect on port 5555

This way port 5555 stays working like it used to.
"""
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import os
import re

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tailscape_last_ip")
PORT = "5555"


def load_last_ip():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return ""


def save_last_ip(ip):
    with open(CONFIG_FILE, "w") as f:
        f.write(ip)


def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = result.stdout.strip()
    if result.stderr:
        output += "\n" + result.stderr.strip()
    return output


def is_connected(result_text):
    low = result_text.lower()
    return "connected" in low and "refused" not in low and "failed" not in low


def scan_for_adb_port(ip):
    """Use nmap to find open ports in the Wireless Debugging range."""
    result = subprocess.run(
        ["nmap", "-p", "30000-50000", "-T4", "--open", ip],
        text=True, capture_output=True
    )
    ports = []
    for match in re.finditer(r"(\d+)/tcp\s+open", result.stdout):
        ports.append(int(match.group(1)))
    return ports


def restore_port_5555(ip, temp_port):
    """Connect via temp port, run tcpip 5555, then reconnect on 5555."""
    run_command(f"adb connect {ip}:{temp_port}")
    time.sleep(1)
    run_command(f"adb -s {ip}:{temp_port} tcpip 5555")
    time.sleep(2)
    run_command(f"adb disconnect {ip}:{temp_port}")
    result = run_command(f"adb connect {ip}:5555")
    return result


def main():
    root = tk.Tk()
    root.withdraw()

    last_ip = load_last_ip()
    phone_ip = simpledialog.askstring(
        "ADB over Tailscale",
        "Enter your phone's Tailscale IP (100.x.x.x):",
        initialvalue=last_ip
    )
    if not phone_ip:
        return

    save_last_ip(phone_ip)

    # Restart ADB server
    run_command("adb kill-server")
    run_command("adb start-server")
    time.sleep(1)

    # Try port 5555 directly
    connect_result = run_command(f"adb connect {phone_ip}:{PORT}")

    if is_connected(connect_result):
        device_list = run_command("adb devices")
        messagebox.showinfo("ADB Status",
            f"Connected to {phone_ip}:{PORT}\n\n{device_list}")
        return

    # Port 5555 failed — try to self-heal
    has_nmap = subprocess.run(
        ["which", "nmap"], capture_output=True
    ).returncode == 0

    if has_nmap:
        # Scan for the Wireless Debugging port
        ports = scan_for_adb_port(phone_ip)

        if ports:
            # Try each discovered port, restore 5555 via it
            for port in ports:
                result = restore_port_5555(phone_ip, port)
                if is_connected(result):
                    device_list = run_command("adb devices")
                    messagebox.showinfo("ADB Status",
                        f"Port 5555 was down. Auto-fixed via port {port}.\n"
                        f"Reconnected on {phone_ip}:5555\n\n{device_list}")
                    return

    # Auto-heal failed — tell user what to do
    messagebox.showerror("Connection Failed",
        f"Could not connect to {phone_ip}:5555\n\n"
        "Port 5555 is not listening and auto-recovery failed.\n\n"
        "To fix this:\n"
        "  1. Connect phone via USB\n"
        "  2. Run: adb tcpip 5555\n"
        "  3. Disconnect USB and try again\n\n"
        "OR:\n"
        "  1. On phone: Settings → Developer Options → Wireless Debugging → ON\n"
        "  2. Run this script again (it will auto-scan and fix port 5555)")


if __name__ == "__main__":
    main()
