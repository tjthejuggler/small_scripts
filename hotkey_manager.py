import tkinter as tk
from tkinter import ttk, font as tkFont # Import ttk and font
import json
import os

class HotkeyManager:
    def __init__(self, master):
        self.master = master
        master.title("Hotkey Manager")
        # Window size will be set dynamically by adjust_window_size()

        # --- Darker Theme Setup ---
        dark_bg = "#1c1c1c"
        dark_fg = "#cccccc"  # Slightly dimmer foreground
        entry_bg = "#252525" # Darker entry
        entry_fg = "#cccccc"
        button_bg = "#333333" # Darker button
        button_fg = "#cccccc"
        listbox_bg = "#252525" # Darker listbox
        listbox_fg = "#cccccc"
        select_bg = "#004a80" # Darker selection blue
        highlight_color = "#404040" # For listbox highlight

        master.configure(bg=dark_bg)

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            print("Clam theme not available, using default with manual styling.")
            pass

        # General widget styling for darker theme
        style.configure(".", background=dark_bg, foreground=dark_fg)
        style.configure("TFrame", background=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=dark_fg, padding=(5,5))
        style.configure("TCheckbutton", background=dark_bg, foreground=dark_fg, padding=(2,2)) # Reduced padding for tighter fit
        style.map("TCheckbutton",
                  background=[('active', dark_bg)],
                  indicatorcolor=[('selected', select_bg), ('!selected', entry_bg)], # Use select_bg for selected indicator
                  foreground=[('active', dark_fg)])
        style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg, padding=(5,5), insertcolor=dark_fg, borderwidth=1, relief="sunken")
        style.configure("TButton", background=button_bg, foreground=button_fg, padding=(5,5), borderwidth=1, relief="raised")
        style.map("TButton",
                  background=[('active', '#4A4A4A')], # Lighter on active
                  foreground=[('active', dark_fg)])

        self.hotkeys = []
        self.hotkeys_file = "hotkeys.json"

        # --- Input Fields Frame ---
        self.input_frame = ttk.Frame(master, padding="10", style="TFrame") # Store as self.input_frame
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        master.columnconfigure(0, weight=1)
        self.input_frame.columnconfigure(1, weight=0) # Checkboxes frame
        self.input_frame.columnconfigure(3, weight=1) # Key entry expands

        # Row 0: Modifiers and Key
        self.hotkey_label = ttk.Label(self.input_frame, text="Modifiers:")
        self.hotkey_label.grid(row=0, column=0, sticky="w", padx=(0,5), pady=(5,5))

        modifiers_checkbox_frame = ttk.Frame(self.input_frame, style="TFrame")
        modifiers_checkbox_frame.grid(row=0, column=1, sticky="w", pady=(5,5))

        self.ctrl_var = tk.BooleanVar()
        self.ctrl_check = ttk.Checkbutton(modifiers_checkbox_frame, text="Ctrl", variable=self.ctrl_var)
        self.ctrl_check.pack(side="left", padx=(0,2))

        self.alt_var = tk.BooleanVar()
        self.alt_check = ttk.Checkbutton(modifiers_checkbox_frame, text="Alt", variable=self.alt_var)
        self.alt_check.pack(side="left", padx=(0,2))

        self.shift_var = tk.BooleanVar()
        self.shift_check = ttk.Checkbutton(modifiers_checkbox_frame, text="Shift", variable=self.shift_var)
        self.shift_check.pack(side="left", padx=(0,2))

        self.meta_var = tk.BooleanVar()
        self.meta_check = ttk.Checkbutton(modifiers_checkbox_frame, text="Meta", variable=self.meta_var)
        self.meta_check.pack(side="left", padx=(0,10)) # Add some padding after meta

        self.key_label = ttk.Label(self.input_frame, text="Key:")
        self.key_label.grid(row=0, column=2, sticky="w", padx=(10,5), pady=(5,5))
        self.key_entry = ttk.Entry(self.input_frame, width=15) # Adjusted width
        self.key_entry.grid(row=0, column=3, sticky="ew", pady=(5,5))

        # Row 1: Description
        self.description_label = ttk.Label(self.input_frame, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="w", pady=(0,5))
        self.description_entry = ttk.Entry(self.input_frame)
        self.description_entry.grid(row=1, column=1, columnspan=3, sticky="ew", pady=(0,5))

        # Row 2: Script Path
        self.script_path_label = ttk.Label(self.input_frame, text="Script Path:")
        self.script_path_label.grid(row=2, column=0, sticky="w", pady=(0,5))
        self.script_path_entry = ttk.Entry(self.input_frame)
        self.script_path_entry.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(0,5))
        
        # Row 3: Buttons
        buttons_frame = ttk.Frame(self.input_frame, style="TFrame")
        buttons_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(10,5))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        self.add_button = ttk.Button(buttons_frame, text="Add Hotkey", command=self.add_hotkey)
        self.add_button.grid(row=0, column=0, padx=(0,5), sticky="ew")
        
        self.delete_button = ttk.Button(buttons_frame, text="Delete Hotkey", command=self.delete_selected_hotkey, state=tk.DISABLED)
        self.delete_button.grid(row=0, column=1, padx=(5,0), sticky="ew")


        # --- Hotkey Listbox Frame ---
        self.listbox_frame = ttk.Frame(master, padding="10", style="TFrame")
        self.listbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        master.rowconfigure(1, weight=1)
        self.listbox_frame.columnconfigure(0, weight=1)
        self.listbox_frame.rowconfigure(0, weight=1)

        self.hotkey_listbox = tk.Listbox(self.listbox_frame,
                                         bg=listbox_bg, fg=listbox_fg,
                                         selectbackground=select_bg, selectforeground=listbox_fg,
                                         borderwidth=0, highlightthickness=1, highlightcolor=highlight_color,
                                         activestyle='none', exportselection=False) # Added exportselection=False
        self.hotkey_listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.hotkey_listbox.yview, style="Vertical.TScrollbar")
        style.configure("Vertical.TScrollbar", background=button_bg, troughcolor=dark_bg, bordercolor=dark_bg, arrowcolor=dark_fg)
        style.map("Vertical.TScrollbar", background=[('active', '#454545')], gripcount=[('!disabled',1)])
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.hotkey_listbox.config(yscrollcommand=scrollbar.set)
        self.hotkey_listbox.bind('<<ListboxSelect>>', self.on_hotkey_select) # Bind selection event

        # Load Hotkeys and Update UI
        self.load_hotkeys()
        self.update_hotkey_listbox() # This will call adjust_window_size

    def add_hotkey(self):
        ctrl = self.ctrl_var.get()
        alt = self.alt_var.get()
        shift = self.shift_var.get()
        meta = self.meta_var.get()
        key = self.key_entry.get()
        description = self.description_entry.get()
        script_path = self.script_path_entry.get()

        hotkey = ""
        if ctrl:
            hotkey += "Ctrl+"
        if alt:
            hotkey += "Alt+"
        if shift:
            hotkey += "Shift+"
        if meta:
            hotkey += "Meta+"

        hotkey_combo = hotkey + key

        if hotkey_combo and description and script_path:
            self.hotkeys.append({"hotkey": hotkey_combo, "description": description, "script_path": script_path})
            self.update_hotkey_listbox()
            self.save_hotkeys()
            self.clear_entries()

    def load_hotkeys(self):
        if os.path.exists(self.hotkeys_file):
            with open(self.hotkeys_file, "r") as f:
                try:
                    self.hotkeys = json.load(f)
                except json.JSONDecodeError:
                    self.hotkeys = []

    def save_hotkeys(self):
        with open(self.hotkeys_file, "w") as f:
            json.dump(self.hotkeys, f, indent=4)

    def update_hotkey_listbox(self):
        self.hotkey_listbox.delete(0, tk.END)
        for hotkey_data in self.hotkeys:
            description = hotkey_data.get('description', '')
            hotkey_combo = hotkey_data.get('hotkey', '')
            script_path = hotkey_data.get('script_path', '')
            self.hotkey_listbox.insert(tk.END, f"{description} - {hotkey_combo} - {script_path}")
        self.adjust_window_size()

    def on_hotkey_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            self.delete_button.config(state=tk.DISABLED)
            return

        selected_index = selection[0]
        if 0 <= selected_index < len(self.hotkeys):
            selected_data = self.hotkeys[selected_index]
            self.clear_entries() # Clear entries first, also disables delete button temporarily

            self.description_entry.insert(0, selected_data.get("description", ""))
            self.script_path_entry.insert(0, selected_data.get("script_path", ""))

            full_hotkey_str = selected_data.get("hotkey", "")
            parts = full_hotkey_str.split('+')
            
            key_to_set = ""
            modifiers_present = []
            if parts:
                potential_key = parts[-1]
                # Check if the last part is a common key or a modifier name itself
                if potential_key and (len(potential_key) == 1 or potential_key.lower() not in ["control", "alt", "shift", "meta", "ctrl"]): # Single char or not a modifier name
                    key_to_set = potential_key
                    modifiers_present = parts[:-1]
                else: # Only modifiers, or last part IS a modifier
                    key_to_set = ""
                    modifiers_present = parts[:]
                
                self.ctrl_var.set(any(m.lower() == "ctrl" for m in modifiers_present))
                self.alt_var.set(any(m.lower() == "alt" for m in modifiers_present))
                self.shift_var.set(any(m.lower() == "shift" for m in modifiers_present))
                self.meta_var.set(any(m.lower() == "meta" for m in modifiers_present))
            
            self.key_entry.insert(0, key_to_set)
            self.delete_button.config(state=tk.NORMAL) # Enable delete button
        else:
            self.delete_button.config(state=tk.DISABLED)

    def adjust_window_size(self):
        self.master.update_idletasks()

        num_items = self.hotkey_listbox.size()
        lines_to_show = min(num_items, 10) if num_items > 0 else 1
        self.hotkey_listbox.config(height=lines_to_show)
        
        self.master.update_idletasks()

        input_height = self.input_frame.winfo_reqheight()
        # Ensure listbox_frame itself has its size computed based on listbox
        self.listbox_frame.update_idletasks()
        listbox_frame_height = self.listbox_frame.winfo_reqheight()
        
        total_height = input_height + listbox_frame_height + 40 # Padding for window chrome

        max_content_width = 0
        if num_items > 0:
            try:
                # Use tkFont for measuring
                listbox_font_config = self.hotkey_listbox.cget("font")
                active_font = tkFont.Font(font=listbox_font_config)
            except tk.TclError:
                active_font = tkFont.Font(family="sans-serif", size=10) # Default

            for i in range(num_items):
                item_text = self.hotkey_listbox.get(i)
                max_content_width = max(max_content_width, active_font.measure(item_text))
        
        # Add width for scrollbar (if visible) and padding
        # A simple check: if num_items > lines_to_show, scrollbar is likely needed
        scrollbar_width_approx = 20 if num_items > lines_to_show else 0
        listbox_content_width_needed = max_content_width + scrollbar_width_approx + 80 # Increased padding for "slightly wider"

        # Compare with input frame's required width
        input_frame_width_needed = self.input_frame.winfo_reqwidth() + 40 # Ensure input frame has enough space too

        final_width = max(listbox_content_width_needed, input_frame_width_needed, 550) # Adjusted overall min width

        self.master.geometry(f"{int(final_width)}x{int(total_height)}")

    def delete_selected_hotkey(self):
        selection = self.hotkey_listbox.curselection()
        if not selection:
            return
        
        selected_index = selection[0]
        # Ensure index is valid before attempting to delete
        if 0 <= selected_index < len(self.hotkeys):
            del self.hotkeys[selected_index]
            self.save_hotkeys()
            self.update_hotkey_listbox() # This re-populates, re-binds, and re-sizes
            self.clear_entries()         # This will also disable the delete button

    def clear_entries(self):
        self.ctrl_var.set(False)
        self.alt_var.set(False)
        self.shift_var.set(False)
        self.meta_var.set(False)
        self.key_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.script_path_entry.delete(0, tk.END)
        if hasattr(self, 'delete_button'): # Ensure delete_button exists before trying to config
            self.delete_button.config(state=tk.DISABLED)

    #def on_key_press(self, event):
    #    modifiers = ""
    #    if event.state & 0x0004:  # Shift key
    #        modifiers += "Shift+"
    #    if event.state & 0x0008:  # Caps Lock
    #        pass
    #    if event.state & 0x0080: # Control key
    #        modifiers += "Ctrl+"
    #    if event.state & 0x8000: # Alt key
    #        modifiers += "Alt+"
    #    if event.state & 0x0400: # Meta key
    #        modifiers += "Meta+"

    #    self.hotkey_entry.delete(0, tk.END)
    #    self.hotkey_entry.insert(0, modifiers)

root = tk.Tk()
my_gui = HotkeyManager(root)
root.mainloop()