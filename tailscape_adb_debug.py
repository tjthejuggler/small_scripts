#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tailscape_last_ip")

def load_last_ip():
    """Load the last used IP from the config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_ip(ip):
    """Save the last used IP to the config file."""
    with open(CONFIG_FILE, "w") as f:
        f.write(ip)

def run_command(command):
    """Runs a shell command and returns the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    # Combine standard output and any errors
    output = result.stdout.strip()
    if result.stderr:
        output += "\n" + result.stderr.strip()
    return output

def main():
    # Hide the main background window so we only see the popups
    root = tk.Tk()
    root.withdraw()

    # 1. Pop up a dialog box asking for the IP, pre-filled with the last used IP
    last_ip = load_last_ip()
    phone_ip = simpledialog.askstring(
        "ADB over Tailscale",
        "Enter your phone's Tailscale IP (100.x.x.x):",
        initialvalue=last_ip
    )

    # If you hit Cancel or leave it blank, exit gracefully
    if not phone_ip:
        return

    save_last_ip(phone_ip)

    port = "5555"

    # 2. Run the ADB commands silently in the background
    run_command("adb kill-server")
    run_command("adb start-server")
    time.sleep(1) # Give the server a second to wake up
    
    connect_result = run_command(f"adb connect {phone_ip}:{port}")
    device_list = run_command("adb devices")

    # 3. Format the results
    final_message = f"--- Connection Result ---\n{connect_result}\n\n--- Current Devices ---\n{device_list}"

    # 4. Pop up a final window showing you the success/failure
    messagebox.showinfo("ADB Status", final_message)

if __name__ == "__main__":
    main()