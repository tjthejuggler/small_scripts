import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8082
ALARM_STATE_FILE = "/tmp/hoteleyes-alarm-state.json"

# Ensure state file exists and is initialized to disabled by default
if not os.path.exists(ALARM_STATE_FILE):
    with open(ALARM_STATE_FILE, "w") as f:
        json.dump({"enabled": False, "triggered": False}, f)
    os.chmod(ALARM_STATE_FILE, 0o666)

class AlarmWebHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress standard logging to keep terminal clean
        pass

    def do_GET(self):
        if self.path == "/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                with open(ALARM_STATE_FILE, "r") as f:
                    state = json.load(f)
            except Exception:
                state = {"enabled": False, "triggered": False}
            self.wfile.write(json.dumps(state).encode("utf-8"))
            return

        elif self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            # Get the host IP to embed the motion stream (port 8081)
            host_ip = self.headers.get('Host', 'localhost').split(':')[0]
            motion_stream_url = f"http://{host_ip}:8081/"

            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>HotelEyes Live Feed & Alarm Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #ff3b30;
            margin-bottom: 10px;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            text-align: center;
        }}
        .stream-container {{
            position: relative;
            width: 100%;
            padding-top: 56.25%; /* 16:9 Aspect Ratio */
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        .stream-container iframe, .stream-container img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}
        .controls {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        button {{
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }}
        button:active {{
            transform: scale(0.98);
        }}
        .btn-enable {{
            background-color: #34c759;
            color: white;
        }}
        .btn-enable:hover {{
            background-color: #28a745;
        }}
        .btn-disable {{
            background-color: #ff3b30;
            color: white;
        }}
        .btn-disable:hover {{
            background-color: #dc3545;
        }}
        .btn-reset {{
            background-color: #ff9500;
            color: white;
        }}
        .btn-reset:hover {{
            background-color: #e08500;
        }}
        .btn-trigger {{
            background-color: #af0000;
            color: white;
        }}
        .btn-trigger:hover {{
            background-color: #8a0000;
        }}
        .status-panel {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 18px;
        }}
        .status-val {{
            font-weight: bold;
        }}
        .status-enabled {{
            color: #34c759;
        }}
        .status-disabled {{
            color: #ff3b30;
        }}
        .status-triggered {{
            color: #ff9500;
            animation: blink 1s infinite;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>HotelEyes Live Feed</h1>
        <div class="stream-container">
            <!-- Embed the motion stream directly -->
            <img src="{motion_stream_url}" alt="Live Stream (Motion Active)" />
        </div>
        
        <div class="status-panel">
            <div>Alarm System: <span id="alarm-status" class="status-val status-disabled">Disabled</span></div>
            <div style="margin-top: 5px;">Alarm Triggered: <span id="trigger-status" class="status-val">No</span></div>
        </div>

        <div class="controls">
            <button class="btn-enable" onclick="toggleAlarm(true)">Enable Alarm</button>
            <button class="btn-disable" onclick="toggleAlarm(false)">Disable Alarm</button>
            <button class="btn-trigger" onclick="triggerAlarm()">Activate Alarm (Panic)</button>
            <button class="btn-reset" onclick="resetTrigger()">Silence/Reset Alarm</button>
        </div>
    </div>

    <script>
        function updateStatus() {{
            fetch('/state')
                .then(r => r.json())
                .then(data => {{
                    const alarmStatus = document.getElementById('alarm-status');
                    const triggerStatus = document.getElementById('trigger-status');
                    
                    if (data.enabled) {{
                        alarmStatus.textContent = 'Enabled';
                        alarmStatus.className = 'status-val status-enabled';
                    }} else {{
                        alarmStatus.textContent = 'Disabled';
                        alarmStatus.className = 'status-val status-disabled';
                    }}
                    
                    if (data.triggered) {{
                        triggerStatus.textContent = 'YES (ALARM SOUNDING)';
                        triggerStatus.className = 'status-val status-triggered';
                    }} else {{
                        triggerStatus.textContent = 'No';
                        triggerStatus.className = 'status-val';
                    }}
                }});
        }}

        function toggleAlarm(enable) {{
            fetch('/toggle?enable=' + enable, {{ method: 'POST' }})
                .then(() => updateStatus());
        }}

        function resetTrigger() {{
            fetch('/reset', {{ method: 'POST' }})
                .then(() => updateStatus());
        }}

        function triggerAlarm() {{
            fetch('/trigger', {{ method: 'POST' }})
                .then(() => updateStatus());
        }}

        // Poll status every second
        setInterval(updateStatus, 1000);
        updateStatus();
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode("utf-8"))
            return
        else:
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/toggle":
            query = urllib.parse.parse_qs(parsed_url.query)
            enable_param = query.get("enable", ["false"])[0]
            enable = enable_param.lower() == "true"
            
            try:
                with open(ALARM_STATE_FILE, "r") as f:
                    state = json.load(f)
            except Exception:
                state = {"enabled": False, "triggered": False}
                
            state["enabled"] = enable
            if not enable:
                state["triggered"] = False # Automatically turn off trigger if disabled
                
            with open(ALARM_STATE_FILE, "w") as f:
                json.dump(state, f)
                
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif parsed_url.path == "/reset":
            try:
                with open(ALARM_STATE_FILE, "r") as f:
                    state = json.load(f)
            except Exception:
                state = {"enabled": False, "triggered": False}
                
            state["triggered"] = False
            
            with open(ALARM_STATE_FILE, "w") as f:
                json.dump(state, f)
                
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif parsed_url.path == "/trigger":
            try:
                with open(ALARM_STATE_FILE, "r") as f:
                    state = json.load(f)
            except Exception:
                state = {"enabled": False, "triggered": False}
                
            # Force trigger the alarm sound (even if system is disabled, or auto-enable it)
            state["enabled"] = True
            state["triggered"] = True
            
            with open(ALARM_STATE_FILE, "w") as f:
                json.dump(state, f)
                
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Bind to all interfaces so it's accessible via Tailscale/LAN
    with socketserver.TCPServer(("", PORT), AlarmWebHandler) as httpd:
        print(f"Serving alarm control on port {PORT}")
        httpd.serve_forever()
