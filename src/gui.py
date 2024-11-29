import customtkinter as ctk
from luxafor_control import LuxaforControl
from CTkColorPicker import *
import keyboard

class LuxaforGUI:
    def __init__(self):
        self.controller = LuxaforControl()
        self.root = ctk.CTk()
        self.root.title("Luxafor Control")
        self.root.geometry("500x500")
        
        # Handle window close and minimize
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.root.bind("<Unmap>", lambda e: self.minimize_to_tray() if self.root.state() == 'iconic' else None)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Menu bar
        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            self.menu_frame,
            text="Reset to Defaults",
            width=120,
            command=self.reset_colors
        ).pack(side="right", padx=5)
        
        # Colors container
        self.colors_frame = ctk.CTkFrame(self.main_frame)
        self.colors_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_color_grid()
        
        # Effects frame
        self.effects_frame = ctk.CTkFrame(self.main_frame)
        self.effects_frame.pack(fill="x", padx=10, pady=10)
        
        self.create_effects_controls()
        
        # Hotkeys frame
        self.hotkeys_frame = ctk.CTkFrame(self.main_frame)
        self.hotkeys_frame.pack(fill="x", padx=10, pady=10)
        
        self.create_hotkey_controls()

    def create_color_grid(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
            
        row = 0
        col = 0
        
        # Add "Off" button with dummy controls
        self.create_button_with_controls(
            "OFF", None, row, col,
            command=self.controller.turn_off,
            fg_color="#333333",
            hover_color="#444444",
            show_controls=False
        )
        
        col += 1
        
        # Add color buttons
        for color_name, rgb in self.controller.saved_colors.items():
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            self.create_button_with_controls(
                "", rgb, row, col,
                command=lambda c=rgb: self.controller.set_color(*c),
                fg_color=hex_color,
                hover_color=hex_color,
                color_name=color_name
            )
            
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Add new color button with dummy controls
        self.create_button_with_controls(
            "+", None, row if col == 0 else row + 1, 0,
            command=self.add_new_color,
            show_controls=False
        )

    def create_button_with_controls(self, text, color, row, col, command, 
                                  fg_color=None, hover_color=None, 
                                  color_name=None, show_controls=True):
        container = ctk.CTkFrame(self.colors_frame, fg_color="transparent")
        container.grid(row=row, column=col, padx=5, pady=5)
        
        btn = ctk.CTkButton(
            container,
            text=text,
            width=60,
            height=60,
            fg_color=fg_color if fg_color else "gray",
            hover_color=hover_color if hover_color else "darkgray",
            command=command
        )
        btn.pack(side="left")
        
        if show_controls:
            controls = ctk.CTkFrame(container, fg_color="transparent")
            controls.pack(side="left", padx=2)
            
            ctk.CTkButton(
                controls,
                text="⟳",  # or "⚙️"
                width=30,
                height=30,
                command=lambda: self.edit_color(color_name) if color_name else None
            ).pack(pady=1)
            
            ctk.CTkButton(
                controls,
                text="−",  # or "❌"
                width=30,
                height=30,
                fg_color="darkred",
                hover_color="red",
                command=lambda: self.delete_color(color_name) if color_name else None
            ).pack(pady=1)

    def create_effects_controls(self):
        effects = ctk.CTkFrame(self.effects_frame)
        effects.pack(fill="x", pady=5)
        
        self.wave_btn = ctk.CTkButton(
            effects,
            text="🌊 Wave",
            width=80,
            command=self.toggle_wave
        )
        self.wave_btn.pack(side="left", padx=5)
        
        self.strobe_btn = ctk.CTkButton(
            effects,
            text="⚡ Strobe",
            width=80,
            command=self.toggle_strobe
        )
        self.strobe_btn.pack(side="left", padx=5)

    def create_hotkey_controls(self):
        ctk.CTkLabel(self.hotkeys_frame, text="Hotkeys").pack(anchor="w", padx=5, pady=(5,0))
        
        hotkeys_grid = ctk.CTkFrame(self.hotkeys_frame)
        hotkeys_grid.pack(fill="x", padx=5, pady=5)
        
        actions = {
            "Cycle Green/Red/Off": "ctrl+alt+1",
            "Toggle On/Off": "ctrl+alt+2",
            "Next Color": "ctrl+alt+3"
        }
        
        row = 0
        for action, default_key in actions.items():
            ctk.CTkLabel(hotkeys_grid, text=action).grid(row=row, column=0, padx=5, pady=2)
            
            entry = ctk.CTkEntry(hotkeys_grid, width=100)
            entry.insert(0, default_key)
            entry.grid(row=row, column=1, padx=5, pady=2)
            
            row += 1

    def toggle_wave(self):
        self.controller.wave_active = not self.controller.wave_active
        if self.controller.wave_active:
            self.wave_btn.configure(fg_color="darkblue")
            if self.controller.current_color:
                self.controller.wave_effect(*self.controller.current_color)
            else:
                self.controller.wave_effect()
        else:
            self.wave_btn.configure(fg_color=None)
            if self.controller.last_color:
                self.controller.set_color(*self.controller.last_color)
            else:
                self.controller.turn_off()

    def toggle_strobe(self):
        self.controller.strobe_active = not self.controller.strobe_active
        if self.controller.strobe_active:
            self.strobe_btn.configure(fg_color="darkblue")
            if self.controller.current_color:
                self.controller.strobe_effect(*self.controller.current_color)
            else:
                self.controller.strobe_effect()
        else:
            self.strobe_btn.configure(fg_color=None)
            if self.controller.last_color:
                self.controller.set_color(*self.controller.last_color)
            else:
                self.controller.turn_off()

    def minimize_to_tray(self):
        self.root.withdraw()

    def reset_colors(self):
        self.controller.reset_to_defaults()
        self.create_color_grid()

    def delete_color(self, color_name):
        del self.controller.saved_colors[color_name]
        self.controller.save_config()
        self.create_color_grid()

    def edit_color(self, color_name):
        picker = AskColor()
        new_color = picker.get()
        if new_color:
            rgb = [int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)]
            self.controller.saved_colors[color_name] = rgb
            self.controller.save_config()
            self.create_color_grid()

    def add_new_color(self):
        picker = AskColor()
        new_color = picker.get()
        if new_color:
            rgb = [int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)]
            color_name = f"Color {len(self.controller.saved_colors) + 1}"
            self.controller.saved_colors[color_name] = rgb
            self.controller.save_config()
            self.create_color_grid()

    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+alt+1', self.controller.cycle_green_red_off)
        keyboard.add_hotkey('ctrl+alt+2', lambda: self.controller.restore_last_color() 
                          if not self.controller.current_color 
                          else self.controller.turn_off())
        keyboard.add_hotkey('ctrl+alt+3', lambda: self.controller.set_color(*self.controller.get_next_color()))

    def run(self):
        self.setup_hotkeys()
        self.root.mainloop()
