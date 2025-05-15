#!/usr/bin/env python3

import sys
import os
import configparser
from pathlib import Path
import subprocess
import pyperclip
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu,
                            QFileDialog, QStyle, QAction) # Added QAction
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from functools import partial # Added for connecting signals with arguments

class FileFinder(QObject):
    MAX_RECENT_PATHS = 10
    RECENT_PATHS_CONFIG_KEY = 'recent_paths'

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.config_dir = os.path.expanduser("~/.config/file_finder_tray")
        self.config_file = os.path.join(self.config_dir, "config.ini")
        
        self.recent_paths = [] # Initialize before init_config
        self.init_config() # This will load/initialize root_path and recent_paths
        
        # Create system tray icon with parent
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set icon with fallback to system icon if file doesn't exist
        icon_path = "placeholder_icon.png"
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(self.app.style().standardIcon(QStyle.SP_FileIcon))
        
        # Create the tray menu
        self.menu = QMenu()
        self.root_path_action = self.menu.addAction(f"Root Path: {self.get_root_path()}")
        self.root_path_action.triggered.connect(self.change_root_path)

        # Recent Paths Submenu
        self.recent_paths_menu = QMenu("Recent Directories", self.menu)
        self.menu.addMenu(self.recent_paths_menu)
        self._update_recent_paths_menu() # Populate it initially

        self.menu.addSeparator()
        refresh_action = self.menu.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh_app)
        self.menu.addSeparator()
        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.icon_activated)
        self.tray_icon.show()

    def init_config(self):
        """Initialize configuration file and directory, including recent paths."""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            self.config = configparser.ConfigParser()
            self.recent_paths = [] # Ensure it's a list

            config_file_existed = os.path.exists(self.config_file)

            if not config_file_existed:
                default_root = os.path.expanduser("~")
                self.config['Settings'] = {
                    'root_path': default_root,
                    self.RECENT_PATHS_CONFIG_KEY: default_root # Start with default in recent
                }
                with open(self.config_file, 'w') as f:
                    self.config.write(f)
            
            # Read the config (either newly created or existing)
            self.config.read(self.config_file)

            # Ensure 'Settings' section and 'root_path' exist, providing defaults if not
            if not self.config.has_section('Settings'):
                self.config.add_section('Settings')
            if not self.config.has_option('Settings', 'root_path'):
                self.config.set('Settings', 'root_path', os.path.expanduser("~"))
            
            # Load recent paths from config
            raw_recent_paths = self.config.get('Settings', self.RECENT_PATHS_CONFIG_KEY, fallback='')
            if raw_recent_paths:
                self.recent_paths = [p.strip() for p in raw_recent_paths.split(',') if p.strip()]
            
            # Ensure current root_path is at the top of recent_paths list and save.
            # This also handles initial population if recent_paths was empty or needed consistency.
            current_root = self.get_root_path() # Relies on self.config being loaded
            self._add_recent_path(current_root) # This adds, orders, trims, and saves config.

        except Exception as e:
            print(f"Error initializing config: {str(e)}")

    def _save_config(self):
        """Save the current configuration (including recent paths) to file."""
        try:
            # Ensure the recent_paths list in config is up-to-date
            self.config.set('Settings', self.RECENT_PATHS_CONFIG_KEY, ','.join(self.recent_paths))
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        except Exception as e:
            print(f"Error saving config: {str(e)}")

    def _add_recent_path(self, path):
        """Adds a path to the recent paths list, keeps it sorted and capped."""
        if not path: # Do not add empty or None paths
            return
            
        try:
            # Remove if exists to move to top
            if path in self.recent_paths:
                self.recent_paths.remove(path)
            
            # Add to the beginning (most recent)
            self.recent_paths.insert(0, path)
            
            # Limit to MAX_RECENT_PATHS
            self.recent_paths = self.recent_paths[:self.MAX_RECENT_PATHS]
            
            # Persist changes
            self._save_config()
        except Exception as e:
            print(f"Error adding recent path '{path}': {str(e)}")


    def _update_recent_paths_menu(self):
        """Clears and rebuilds the recent paths submenu."""
        self.recent_paths_menu.clear()
        if not self.recent_paths:
            no_recent_action = self.recent_paths_menu.addAction("No recent directories")
            no_recent_action.setEnabled(False)
        else:
            for path in self.recent_paths:
                action = QAction(path, self.recent_paths_menu) # Parent is submenu
                # Use partial to pass the path argument to the slot
                action.triggered.connect(partial(self._set_root_path_from_recent, path))
                self.recent_paths_menu.addAction(action)

    def _set_root_path_from_recent(self, path):
        """Sets the root path when a recent directory is selected from the submenu."""
        try:
            self.config.set('Settings', 'root_path', path) # Update in-memory config
            self.root_path_action.setText(f"Root Path: {path}")
            
            # This will move 'path' to the top of recent_paths, trim, and save config
            self._add_recent_path(path) 
            
            self._update_recent_paths_menu() # Refresh the menu to reflect new order
            self.show_notification("Root Path Changed", f"Root path set to: {path}")
        except Exception as e:
            print(f"Error setting root path from recent: {str(e)}")
            self.show_notification("Error", "Could not set root path from recent list.")


    def get_root_path(self):
        """Get the current root path from config"""
        try:
            # Ensure Settings section and root_path option exist before getting
            if not self.config.has_section('Settings'):
                self.config.add_section('Settings')
            if not self.config.has_option('Settings', 'root_path'):
                 self.config.set('Settings', 'root_path', os.path.expanduser("~"))
            return self.config.get('Settings', 'root_path')
        except Exception: # Fallback if any error occurs
            return os.path.expanduser("~")

    def change_root_path(self):
        """Open directory dialog to change root path"""
        try:
            current_path = self.get_root_path()
            # Pass self.menu as parent for the dialog if desired, or None
            new_path = QFileDialog.getExistingDirectory(
                self.menu, # Or None
                "Select Root Directory",
                current_path,
                QFileDialog.ShowDirsOnly
            )
            
            if new_path:
                self.config.set('Settings', 'root_path', new_path) # Update in-memory config
                self.root_path_action.setText(f"Root Path: {new_path}")
                
                # This will add to recent, reorder, trim, and save the entire config
                self._add_recent_path(new_path) 
                
                self._update_recent_paths_menu() # Update the menu display
                self.show_notification("Root Path Changed", f"Root path set to: {new_path}")
        except Exception as e:
            print(f"Error changing root path: {str(e)}")

    def get_selected_text(self):
        """Get system-wide selected text using multiple methods"""
        # Try PyQt clipboard first
        try:
            clipboard = QApplication.clipboard()
            text = clipboard.text(mode=clipboard.Selection)  # Try to get X11 selection
            if text:
                return text.strip()
        except Exception as e:
            print(f"PyQt clipboard error: {str(e)}")

        # Try pyperclip as fallback
        try:
            text = pyperclip.paste()
            if text:
                return text.strip()
        except Exception as e:
            print(f"Pyperclip error: {str(e)}")

        # Try xclip as last resort
        try:
            result = subprocess.run(
                ['xclip', '-o', '-selection', 'primary'],
                capture_output=True,
                text=True
            )
            if result.stdout:
                return result.stdout.strip()
        except Exception as e:
            print(f"xclip error: {str(e)}")

        self.show_notification("Error", "Failed to get selected text")
        return None

    def extract_filenames(self, text):
        """Extract potential filenames from text based on common file extensions"""
        print("\nDEBUG: Analyzing clipboard text:")
        print(f"'{text}'")
        
        # Common file extensions
        valid_extensions = {
            'txt', 'py', 'md', 'json', 'ini', 'cfg', 'yaml', 'yml', 'xml',
            'html', 'css', 'js', 'jsx', 'ts', 'tsx', 'cpp', 'hpp', 'c', 'h',
            'kt', 'java', 'go', 'rs', 'rb', 'php', 'sh', 'bash', 'sql', 'conf',
            'toml', 'log', 'gradle', 'properties', 'swift', 'scala', 'r', 'pl',
            'lua', 'dart', 'm', 'mm', 'cs', 'vb', 'fs', 'ex', 'exs', 'clj',
            'groovy', 'pas', 'adb', 'ads', 'asm', 's', 'f90', 'f95', 'f03',
            'for', 'erl', 'hrl', 'pm'
        }

        # Split text by common separators
        words = text.replace(',', ' ').split()
        
        # Filter for valid filenames
        matches = []
        print("\nDEBUG: Processing words:")
        for word in words:
            # Handle paths by extracting the last component
            path_parts = word.replace('\\', '/').split('/')
            potential_filename = path_parts[-1]
            
            # Remove any trailing parenthetical content like "(Phone)"
            if '(' in potential_filename:
                potential_filename = potential_filename.split('(')[0].strip()
            
            if '.' in potential_filename:  # Must have an extension
                name, ext = potential_filename.rsplit('.', 1)
                if name and ext.lower() in valid_extensions:  # Must have name and valid extension
                    print(f"Found valid filename: '{potential_filename}' from '{word}'")
                    # Store both the original path and the extracted filename
                    matches.append((word, potential_filename))
                else:
                    print(f"Skipping invalid filename: '{potential_filename}' from '{word}'")
            else:
                print(f"Skipping no extension: '{potential_filename}' from '{word}'")
        
        print("\nDEBUG: Final matches:", matches if matches else "None")
        return matches

    def find_files(self, filename_tuples):
        """Find multiple files by name match in root directory"""
        if not filename_tuples:
            return [], "empty"
            
        root_path = Path(self.get_root_path())
        found_files = []
        not_found = []
        
        try:
            for original_path, filename in filename_tuples:
                print(f"Searching for '{filename}' (from '{original_path}')")
                
                # First try: exact match with the original path
                exact_matches = list(root_path.rglob(original_path))
                if exact_matches:
                    print(f"Found exact match: {exact_matches[0]}")
                    found_files.append(exact_matches[0])
                    continue
                
                # Second try: search for the filename only
                basename_matches = list(root_path.rglob(filename))
                if basename_matches:
                    print(f"Found by basename: {basename_matches[0]}")
                    found_files.append(basename_matches[0])
                    continue
                
                # Third try: search for partial path match
                # Split the original path into components
                path_parts = original_path.replace('\\', '/').split('/')
                
                # Try to match increasingly longer path segments from the end
                found = False
                for i in range(1, min(len(path_parts) + 1, 5)):  # Limit to 4 segments for performance
                    partial_path_str = '/'.join(path_parts[-i:]) # Renamed to avoid conflict
                    print(f"Trying partial path: {partial_path_str}")
                    
                    # Use ** wildcard to match any directory structure
                    partial_matches = list(root_path.glob(f"**/{partial_path_str}"))
                    if partial_matches:
                        print(f"Found by partial path: {partial_matches[0]}")
                        found_files.append(partial_matches[0])
                        found = True
                        break
                
                if not found:
                    not_found.append(original_path)
                    
            if not found_files:
                return [], "not_found"
            return found_files, "found" if not not_found else "partial"
            
        except Exception as e:
            print(f"Error searching for files: {str(e)}")
            return [], "error"

    def show_notification(self, title, message, duration=5000):
        """Show a system tray notification"""
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, duration)

    def copy_files_info(self, file_paths):
        """Copy paths and contents of multiple files to clipboard"""
        result = []
        paths_only = []
        errors = []
        
        for file_path_obj in file_paths: # file_paths are Path objects
            try:
                with open(file_path_obj, 'r', encoding='utf-8') as f: # Added encoding
                    content = f.read()
                result.append(f"=== {str(file_path_obj)} ===\n{content}\n")
            except Exception as e:
                print(f"Error reading file {file_path_obj}: {str(e)}")
                try:
                    paths_only.append(str(file_path_obj))
                except: # Should not happen for str(Path)
                    errors.append(str(file_path_obj)) # Fallback
        
        combined = "\n".join(result)
        if paths_only:
            combined += "\n=== PATHS ONLY (could not read content) ===\n"
            combined += "\n".join(paths_only)
            
        if combined:
            try:
                pyperclip.copy(combined)
                return "full" if not paths_only and not errors else "partial"
            except Exception as e:
                print(f"Error copying to clipboard: {str(e)}")
                # If pyperclip fails, it might raise pyperclip.PyperclipException
                # or other OS-specific errors.
                self.show_notification("Clipboard Error", "Failed to copy to clipboard. Is xclip/xsel installed?")
                return False # Indicate failure
        return False if errors else True # True if no content but paths copied successfully

    def icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            selected_text = self.get_selected_text()
            if not selected_text:
                self.show_notification("Error", "No text selected")
                return
                
            filename_tuples = self.extract_filenames(selected_text)
            if not filename_tuples:
                self.show_notification(
                    "No Files Found",
                    "No valid filenames found in selected text"
                )
                return
                
            found_files, status = self.find_files(filename_tuples)
            
            if status == "not_found":
                self.show_notification(
                    "Files Not Found",
                    f"No files found matching: {', '.join([original for original, _ in filename_tuples])}"
                )
            elif status in ["found", "partial"]:
                copy_result = self.copy_files_info(found_files)
                if copy_result == "full":
                    self.show_notification(
                        "Files Found",
                        f"Found and copied {len(found_files)} files"
                    )
                elif copy_result == "partial":
                    self.show_notification(
                        "Partial Success",
                        f"Copied info for {len(found_files)} files. Some contents might be missing."
                    )
                else: # False from copy_files_info means clipboard error
                    self.show_notification(
                        "Error",
                        "Found files, but failed to copy information to clipboard."
                    )
            elif status == "error":
                 self.show_notification("Error", "An error occurred while searching for files.")


    def refresh_app(self):
        """Restart the application to apply code changes"""
        self.show_notification("Refreshing", "Restarting application to apply changes...")
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start_file_finder.sh")
        if os.path.exists(script_path) and os.access(script_path, os.X_OK):
            subprocess.Popen([script_path])
            QApplication.quit()
        else:
            self.show_notification("Refresh Error", f"Script not found or not executable: {script_path}")
            print(f"Refresh Error: Script not found or not executable: {script_path}")

        
    def quit_app(self):
        """Quit the application"""
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Important for tray apps
    # Style might be set here if desired, e.g., app.setStyle("Fusion")
    
    # It's good practice to set application name and version for some DE integrations
    app.setApplicationName("FileFinderTray")
    app.setOrganizationName("YourNameOrOrg") # Optional
    
    file_finder = FileFinder(app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()