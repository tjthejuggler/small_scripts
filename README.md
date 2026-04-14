# Small Scripts Collection

A collection of useful utility scripts for various tasks.

*Last updated: 2026-04-14T18:18:21Z*

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
- **Audio & System Scripts**: `fix_audio.sh`, `restart_audio_services.sh`, `refresh_mouse.sh`
- **Clipboard & Text Processing**: `clipboard_newlines.py`, `extract_text_from_selection.py`, `selection_translator.py`
- **File Management**: `file_finder_tray.py`, `launch-or-activate.sh`
- **Habit Tracking**: `obsid_habits_scrape.py`, `scrape_loop_habits.py`, `total_and_pending_habits.py`
- **Hotkey Management**: `hotkey_manager.py`, `run_hotkey_manager.sh`
- **Mouse & Display**: `mouse_position_toggle.py`, `toggle_mouse.sh`, `cycle-backlight.sh`
- **Todo Management**: `todoCounter-increase.py`, `random_todo_item.py`
- **Wallpaper Scripts**: Various scripts in `wallpaper-scripts/` directory
- **Word Processing**: `frequent_words.py`, `state_wordsearch.py`

## Installation & Setup

1. Clone or download the scripts
2. Install Python dependencies: `pip install -r requirements.txt`
3. Make scripts executable: `chmod +x *.py *.sh`
4. Run individual scripts as needed

## Contributing

Feel free to add new utility scripts or improve existing ones. Keep scripts modular and well-documented.