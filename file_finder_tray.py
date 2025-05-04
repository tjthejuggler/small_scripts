#!/usr/bin/env python3

import sys
import os
import configparser
from pathlib import Path
import subprocess
import pyperclip
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu,
                            QFileDialog, QStyle)
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon

class FileFinder(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.config_dir = os.path.expanduser("~/.config/file_finder_tray")
        self.config_file = os.path.join(self.config_dir, "config.ini")
        self.init_config()
        
        # Create system tray icon with parent
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set icon with fallback to system icon if file doesn't exist
        icon_path = "placeholder_icon.png"
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Use a system icon as fallback
            self.tray_icon.setIcon(self.app.style().standardIcon(QStyle.SP_FileIcon))
        
        # Create the tray menu with parent
        self.menu = QMenu()  # No parent needed since FileFinder is a QObject, not a QWidget
        self.root_path_action = self.menu.addAction(f"Root Path: {self.get_root_path()}")
        self.root_path_action.triggered.connect(self.change_root_path)
        self.menu.addSeparator()
        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        # Set up the tray icon
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.icon_activated)
        self.tray_icon.show()

    def init_config(self):
        """Initialize configuration file and directory"""
        try:
            # Create config directory if it doesn't exist
            os.makedirs(self.config_dir, exist_ok=True)
            
            self.config = configparser.ConfigParser()
            
            # If config file doesn't exist, create it with default values
            if not os.path.exists(self.config_file):
                self.config['Settings'] = {
                    'root_path': os.path.expanduser("~")
                }
                with open(self.config_file, 'w') as f:
                    self.config.write(f)
            else:
                self.config.read(self.config_file)
                
        except Exception as e:
            print(f"Error initializing config: {str(e)}")

    def get_root_path(self):
        """Get the current root path from config"""
        try:
            return self.config.get('Settings', 'root_path')
        except:
            return os.path.expanduser("~")

    def change_root_path(self):
        """Open directory dialog to change root path"""
        try:
            current_path = self.get_root_path()
            new_path = QFileDialog.getExistingDirectory(
                None,
                "Select Root Directory",
                current_path,
                QFileDialog.ShowDirsOnly
            )
            
            if new_path:
                self.config['Settings']['root_path'] = new_path
                with open(self.config_file, 'w') as f:
                    self.config.write(f)
                self.root_path_action.setText(f"Root Path: {new_path}")
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
            if '.' in word:  # Must have an extension
                name, ext = word.rsplit('.', 1)
                if name and ext.lower() in valid_extensions:  # Must have name and valid extension
                    print(f"Found valid filename: '{word}'")
                    matches.append(word)
                else:
                    print(f"Skipping invalid filename: '{word}'")
            else:
                print(f"Skipping no extension: '{word}'")
        
        print("\nDEBUG: Final matches:", matches if matches else "None")
        return matches

    def find_files(self, filenames):
        """Find multiple files by exact name match in root directory"""
        if not filenames:
            return [], "empty"
            
        root_path = Path(self.get_root_path())
        found_files = []
        not_found = []
        
        try:
            for filename in filenames:
                matches = list(root_path.rglob(filename))
                if matches:
                    # Take the first match for each filename
                    found_files.append(matches[0])
                else:
                    not_found.append(filename)
                    
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
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                result.append(f"=== {str(file_path)} ===\n{content}\n")
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                try:
                    # If we can't read content, just add the path
                    paths_only.append(str(file_path))
                except:
                    errors.append(str(file_path))
        
        # Combine results
        combined = "\n".join(result)
        if paths_only:
            combined += "\n=== PATHS ONLY (could not read content) ===\n"
            combined += "\n".join(paths_only)
            
        if combined:
            try:
                pyperclip.copy(combined)
                return "full" if not paths_only else "partial"
            except Exception as e:
                print(f"Error copying to clipboard: {str(e)}")
                return False
        return False if errors else True

    def icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            selected_text = self.get_selected_text()
            if not selected_text:
                self.show_notification("Error", "No text selected")
                return
                
            filenames = self.extract_filenames(selected_text)
            if not filenames:
                self.show_notification(
                    "No Files Found",
                    "No valid filenames found in selected text"
                )
                return
                
            found_files, status = self.find_files(filenames)
            
            if status == "not_found":
                self.show_notification(
                    "Files Not Found",
                    f"No files found matching: {', '.join(filenames)}"
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
                        f"Some files were found but not all contents could be read"
                    )
                else:
                    self.show_notification(
                        "Error",
                        "Failed to copy file information"
                    )

    def quit_app(self):
        """Quit the application"""
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    file_finder = FileFinder(app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()