# Mouse Mode Switching System

This system allows switching between different sets of mouse button configurations by pressing the volume up button when no volume button has been pressed in the last 5 seconds.

## Directory Structure

```
mouse_modes/
├── default/           # Default mode scripts
│   ├── upper_left.sh
│   ├── lower_left.sh
│   ├── upper_right.sh
│   └── lower_middle.sh
├── alternate/         # Alternate mode scripts (placeholders)
│   ├── upper_left.sh
│   ├── lower_left.sh
│   ├── upper_right.sh
│   └── lower_middle.sh
├── custom_mode/       # Custom mode scripts (example)
│   ├── upper_left.sh
│   ├── lower_left.sh
│   ├── upper_right.sh
│   └── lower_middle.sh
└── mode_manager.sh    # Main script that manages modes
```

## Button Scripts

The following scripts should be mapped to your mouse buttons in KDE shortcuts:

- `button_upper_left.sh` - Upper left mouse button
- `button_lower_left.sh` - Lower left mouse button
- `button_upper_right.sh` - Upper right mouse button
- `button_lower_middle.sh` - Lower middle mouse button
- `button_volume_up.sh` - Volume up mouse button
- `button_volume_down.sh` - Volume down mouse button

## How It Works

1. When a mouse button is pressed, the corresponding button script calls the mode manager with the button name.
2. The mode manager checks the current mode and executes the appropriate script from the mode directory.
3. For volume buttons, the mode manager also tracks when they were last pressed.
4. If the volume up button is pressed and no volume button has been pressed in the last 5 seconds, the mode is switched to the next one.
5. A notification is displayed when the mode is switched.

## Adding New Modes

To add a new mode:

1. Create a new directory under `mouse_modes/` with the mode name.
2. Add scripts for each button in the new directory.
3. Update the `MODES` array in `mode_manager.sh` to include the new mode.

## Current Button Mappings

### Default Mode
- Upper Left: Launches or focuses Obsidian
- Lower Left: Launches or focuses VS Code
- Upper Right: Launches or focuses Firefox
- Lower Middle: Launches or focuses Konsole
- Volume Up: Increases volume by 10%
- Volume Down: Decreases volume by 10%

### Alternate Mode
- All buttons show a notification indicating which button was pressed in alternate mode
- Volume buttons still control volume but also show the alternate mode notification

### Custom Mode
- Example mode showing how to add additional modes
- All buttons show a notification indicating which button was pressed in custom mode
- You can replace these scripts with your own functionality