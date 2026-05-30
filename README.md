# Small Scripts Collection

A collection of useful utility scripts for various tasks.

*Last updated: 2026-05-29T21:14:00Z*

## PDF Splitter

### Description
`pdf_splitter.py` - Split a PDF into multiple smaller PDFs based on page ranges.

### Features
- Split PDFs based on a list of page numbers
- Automatic page range calculation
- Proper error handling and validation
- Command-line interface with helpful options
- Descriptive output filenames

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python pdf_splitter.py <pdf_file> <page_numbers> [options]
```

#### Examples
```bash
# Basic usage
python pdf_splitter.py document.pdf 1,7,20,32,45

# With custom output directory
python pdf_splitter.py document.pdf 1,7,20,32,45 --output-dir ./splits

# With verbose output
python pdf_splitter.py document.pdf 1,7,20,32,45 --verbose
```

#### How it works
If you provide page numbers `1,7,20,32,45`, the program will create:
- `document_part_1_pages_2-7.pdf` (pages 2-7)
- `document_part_2_pages_8-20.pdf` (pages 8-20)
- `document_part_3_pages_21-32.pdf` (pages 21-32)
- `document_part_4_pages_33-45.pdf` (pages 33-45)

Each PDF contains pages starting after the previous number and ending at (and including) the next number in the list.

#### Options
- `--output-dir, -o`: Specify output directory for split PDFs
- `--verbose, -v`: Enable verbose output
- `--help, -h`: Show help message

### Dependencies
- `pypdf>=3.0.0`

## ADB over Tailscale

### Description
`tailscape_adb_debug.py` - GUI script to connect to an Android phone via ADB over a Tailscale network on port 5555.

### Features
- Remembers the last used Tailscale IP
- Connects on port 5555 (fast, simple, like it should be)
- **Self-healing**: if port 5555 is down (e.g. after phone reboot), auto-discovers the Wireless Debugging random port via `nmap`, connects on it, runs `adb tcpip 5555` to restore port 5555, then reconnects
- **Timeout-protected**: all subprocess calls have timeouts (10s for ADB, 30s for nmap) so the script can never hang indefinitely
- **Force-kill fallback**: if `adb kill-server` hangs (stuck ADB server), the script force-kills the server process and continues

### Usage
```bash
python tailscape_adb_debug.py
```

### Initial Setup (one-time)
1. Connect phone via USB
2. Run `adb tcpip 5555` — this enables port 5555 on the phone
3. Disconnect USB — port 5555 persists until the phone reboots

If the phone reboots and port 5555 stops, the script auto-fixes it as long as Wireless Debugging is enabled on the phone.

### Dependencies
- `nmap` (recommended, for auto port recovery): `sudo apt install nmap`

## Other Scripts

This directory contains various utility scripts for different purposes:

- **ADB & Device**: `tailscape_adb_debug.py`
- **Audio & System Scripts**: `record_laptop_audio.sh`, `fix_audio.sh`, `restart_audio_services.sh`, `refresh_mouse.sh`, `vlc_toggle.sh`
- **Clipboard & Text Processing**: `clipboard_newlines.py`, `extract_text_from_selection.py`, `selection_translator.py`
- **File Management**: `file_finder_tray.py`, `launch-or-activate.sh`
- **Habit Tracking**: `obsid_habits_scrape.py`, `scrape_loop_habits.py`, `total_and_pending_habits.py`
- **Hotkey Management**: `hotkey_manager.py`, `run_hotkey_manager.sh`
- **Mouse & Display**: `mouse_position_toggle.py`, `toggle_mouse.sh`, `cycle-backlight.sh`
- **Todo Management**: `todoCounter-increase.py`, `random_todo_item.py`
- **Wallpaper Scripts**: Various scripts in `wallpaper-scripts/` directory
- **Word Processing**: `frequent_words.py`, `state_wordsearch.py`
- **HotelEyes Security Camera**: `/opt/hoteleyes/hoteleyes.sh` - Security camera system with motion detection, Telegram notifications, delayed multi-frame capture, live stream, and web-controlled alarm system.

## VLC Toggle

### Description
`vlc_toggle.sh` - Toggle VLC media player play/pause. If VLC is not running, launches it.

### Usage
```bash
./vlc_toggle.sh
```

### How it works
Uses the MPRIS2 D-Bus interface (`org.mpris.MediaPlayer2.vlc`) to send a `PlayPause` signal. If VLC is not on the session bus, it launches VLC in the background. No dependencies beyond a standard Linux desktop with D-Bus.

## Laptop Audio Recorder

### Description
`record_laptop_audio.sh` - Record system audio output even when the physical volume is turned down or muted. Perfect for long-running recordings (e.g., 6.5 hours) without disturbing others.

### Features
- **Silent Recording**: Creates a virtual null sink and routes all system audio to it. You can safely mute or turn down your laptop speakers, and the recording will still capture everything at full volume.
- **Loopback Support**: Automatically sets up a loopback so you can still hear the audio if you turn up your physical volume.
- **Auto-routing**: Automatically moves all currently playing audio streams to the virtual sink when recording starts, and restores them when finished.
- **Configurable Duration**: Supports flexible duration formats (e.g., `6.5h`, `30m`, `120s`, or raw seconds).
- **On-the-fly Compression**: Encodes directly to high-quality MP3 (192 kbps) to save gigabytes of disk space over long recording sessions.
- **Graceful Cleanup**: Uses a robust signal trap to ensure that even if interrupted (Ctrl+C), the script restores your original audio configuration and unloads virtual modules.

### Usage
```bash
./record_laptop_audio.sh [duration] [output_file]
```

#### Examples
```bash
# Record for 6.5 hours (default) and save to a timestamped MP3 file
./record_laptop_audio.sh

# Record for 6.5 hours and save to a specific file
./record_laptop_audio.sh 6.5h my_lecture.mp3

# Record for 30 minutes
./record_laptop_audio.sh 30m meeting.mp3

# Record for 10 seconds (quick test)
./record_laptop_audio.sh 10s test.mp3
```

### Dependencies
- `ffmpeg` (with PulseAudio support)
- `pactl` (PulseAudio/PipeWire control utility)
- `bc` (arbitrary precision calculator)

## Installation & Setup

1. Clone or download the scripts
2. Install Python dependencies: `pip install -r requirements.txt`
3. Make scripts executable: `chmod +x *.py *.sh`
4. Run individual scripts as needed

## Contributing

Feel free to add new utility scripts or improve existing ones. Keep scripts modular and well-documented.