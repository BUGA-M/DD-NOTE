import customtkinter as ctk
from Frontend import ConnexionFrame
from Custom import FontInstaller,CreatFrame,CreatLabel,CreatButton
from PIL import Image
import json
import os
import sys
import subprocess
from tkinter import messagebox

class ThemeManager:
    CONFIG_FILE = "app_config.json"

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
            
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.install_fonts()
        self.load_frames()

    def setup_window(self):
        self.geometry("1280x720")
        self.minsize(500, 750)
        self.title("DDnote")
        #self.config(bg="#1e293b")
        
        ######-------- ajou -----#####
        self.config = ThemeManager.load_theme_preference()

        ctk.set_appearance_mode(self.config["theme"])
        ctk.set_default_color_theme(self.config["color_theme"])

        self.theme_var = ctk.StringVar(value=self.config["theme"])
        self.color_theme_var = ctk.StringVar(value=self.config["color_theme"])
        
        self.Frame_theme_controls()

    def install_fonts(self):
        FontInstaller.installerFont("Titan One", "Custom/db_fonts/TitanOne-Regular.ttf", 50)
        FontInstaller.installerFont("Poppins", "Custom/db_fonts/Poppins-Regular.ttf", 22)
        FontInstaller.installerFont("Orbitron", "Custom/db_fonts/static/Orbitron-Bold.ttf", 22)
        
    def load_frames(self):
        self.connexion_frame = ConnexionFrame(self)
        self.connexion_frame.showPack()
        
    #####-------# ajou #---------####
    def Frame_theme_controls(self):
        control_frame = CreatFrame(self,width=100,height=200, corner_radius=8)
        control_frame.FramePack(pady=10, padx=20,fill="x",expand=None)
        
        CreatLabel(control_frame, text="Appearance Mode:").grid(row=0, column=0, padx=10, pady=5)
        theme_menu = ctk.CTkOptionMenu(
            control_frame, values=["system", "light", "dark"], variable=self.theme_var, command=self.change_theme
        )
        theme_menu.grid(row=0, column=1, padx=10, pady=5)

        CreatLabel(control_frame, text="Color Theme:").grid(row=0, column=2, padx=10, pady=5)
        color_menu = ctk.CTkOptionMenu(
            control_frame, values=["blue", "green", "dark-blue"], variable=self.color_theme_var,
            command=self.change_color_theme
        )
        color_menu.grid(row=0, column=3, padx=10, pady=5)

        info_btn = CreatButton(control_frame, text="ℹ️ Info", width=30, command=self.show_info,
                                 fg_color="transparent")
        info_btn.grid(row=0, column=4, padx=10)

    def show_info(self):

        messagebox.showinfo("Theme Switcher",
                            "Professional Theme Management System\n\n• Change themes\n• Switch color schemes\n• Preferences saved automatically")

    def change_theme(self, new_theme):
        if self.winfo_exists():
            ctk.set_appearance_mode(new_theme)
            self.config["theme"] = new_theme
            ThemeManager.save_theme_preference(new_theme, self.config["color_theme"])

    def change_color_theme(self, new_color_theme):
        if self.winfo_exists():
            ctk.set_default_color_theme(new_color_theme)
            self.config["color_theme"] = new_color_theme
            ThemeManager.save_theme_preference(self.config["theme"], new_color_theme)
            self.after(100, self.recreate_app)

    def recreate_app(self):
        if messagebox.askyesno("Restart Required", "Color theme change requires restart. Restart now?"):
            # sys.exit()
            self.quit()
            subprocess.Popen([sys.executable] + sys.argv)

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()



if __name__ == "__main__":
    #ctk.set_appearance_mode("dark")
    #ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
