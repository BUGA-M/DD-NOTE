import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatFrame, CreatLabel, CreatButton
import os
import json

class ThemeColors:
    FILE_PATH = os.path.join(os.path.dirname(__file__), "theme_colors.json")

    @classmethod
    def load_colors(cls, theme_name):
        try:
            with open(cls.FILE_PATH, "r") as f:
                data = json.load(f)
                return data.get(theme_name, data["blue"])  # fallback
        except Exception as e:
            print(f"Erreur chargement thème JSON : {e}")
            return {
                "title": "#3b82f6",
                "subtitle": "#94a3b8",
                "button": "#334155",
                "button_hover": "#0ea5e9",
                "border": "#64748b",
                "footer": "#64748b",
                "control_bg": "#1e293b"  # couleur par défaut du panneau
            }

class ThemeManager:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "Theme_current.json")

    @classmethod
    def load_theme_preference(cls):
        default_prefs = {"theme": "system", "color_theme": "blue"}
        try:
            if os.path.exists(cls.CONFIG_FILE):
                with open(cls.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            return default_prefs
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_prefs

    @classmethod
    def save_theme_preference(cls, theme, color_theme):
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump({"theme": theme, "color_theme": color_theme}, f)
        except Exception as e:
            print(f"Error saving config: {e}")

class ThemeControls:
    def __init__(self, master, config: dict, on_restart_callback):
        self.master = master
        self.config = config
        self.theme_var = ctk.StringVar(value=self.config["theme"])
        self.color_theme_var = ctk.StringVar(value=self.config["color_theme"])
        self.on_restart_callback = on_restart_callback
        self._build_ui()

    def _build_ui(self):
        # Charge les couleurs du thème actuel (pas celles sélectionnées)
        self.theme_data = ThemeColors.load_colors(self.color_theme_var.get())

        self.control_frame = CreatFrame(
            self.master,
            width=100,
            height=200,
            corner_radius=8,
            fg_color=self.theme_data.get("control_bg", "#444")
        )
        self.control_frame.FramePack(pady=10, padx=20, fill="x", expand=None)

        CreatLabel(self.control_frame, text="Appearance Mode:").grid(row=0, column=0, padx=10, pady=5)
        self.theme_menu = ctk.CTkOptionMenu(
            self.control_frame, values=["system", "light", "dark"],
            variable=self.theme_var, command=self.change_theme
        )
        self.theme_menu.grid(row=0, column=1, padx=10, pady=5)

        CreatLabel(self.control_frame, text="Color Theme:").grid(row=0, column=2, padx=10, pady=5)
        self.color_menu = ctk.CTkOptionMenu(
            self.control_frame, values=["blue", "green", "dark-blue"],
            variable=self.color_theme_var, command=self.change_color_theme
        )
        self.color_menu.grid(row=0, column=3, padx=10, pady=5)

        self.info_btn = CreatButton(
            self.control_frame, text="ℹ️ Info", width=30,
            command=self.show_info, fg_color="transparent"
        )
        self.info_btn.grid(row=0, column=4, padx=10)

    def show_info(self):
        messagebox.showinfo(
            "Theme Switcher",
            "Professional Theme Management System\n\n"
            "• Change themes\n• Switch color schemes\n• Preferences saved automatically"
        )

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)
        self.config["theme"] = new_theme
        ThemeManager.save_theme_preference(new_theme, self.config["color_theme"])

    def change_color_theme(self, new_color_theme):
        # Met à jour la config mais n’applique rien visuellement maintenant
        self.config["color_theme"] = new_color_theme
        ThemeManager.save_theme_preference(self.config["theme"], new_color_theme)

        # Demande redémarrage pour appliquer le thème
        self.master.after(100, self.recreate_app)

    def recreate_app(self):
        if messagebox.askyesno("Redémarrage requis", "Le changement de thème nécessite un redémarrage.\nSouhaitez-vous redémarrer maintenant ?"):
            self.on_restart_callback()
