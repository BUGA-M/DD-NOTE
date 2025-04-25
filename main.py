import customtkinter as ctk
from Frontend import ConnexionFrame,Apk
from Custom import FontInstaller,CreatFrame,CreatLabel,CreatButton,ThemeControls,ThemeManager,ThemeColors,ChangeFrame
from PIL import Image
import json
import os
import sys
import subprocess
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.theme_config = ThemeManager.load_theme_preference()
        self.setup_window()
        self.install_fonts()
        self.current_frame=None
        self.FrameSinscrire=[
            lambda parent:Apk(parent,"Enter your code","Enter your password","admin.csv","admin"),
            lambda parent:Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"),
            lambda parent:Apk(parent,"Enter your CIN","Enter your password","Formateur.csv","Formateur")
        ]
        self.manager=ChangeFrame(self)
        self.manager.show_frame(lambda parent:ConnexionFrame(parent,self.FrameSinscrire))
        # self.load_frames()


    def setup_window(self):
        self.geometry("1280x720")
        self.minsize(500, 750)
        self.title("DDnote")

        ctk.set_appearance_mode(self.theme_config["theme"])
        #ctk.set_default_color_theme(self.theme_config["color_theme"])

        self.theme_controls = ThemeControls(self, self.theme_config, self.recreate_app)

    def install_fonts(self):
        FontInstaller.installerFont("Titan One", "Custom/db_fonts/TitanOne-Regular.ttf", 50)
        FontInstaller.installerFont("Poppins", "Custom/db_fonts/Poppins-Regular.ttf", 22)
        FontInstaller.installerFont("Orbitron", "Custom/db_fonts/static/Orbitron-Bold.ttf", 22)

    def load_frames(self):
        self.connexion_frame = ConnexionFrame(self,self.FrameSinscrire)
        self.connexion_frame.showPack()
        


    def recreate_app(self):
        self.quit()
        subprocess.Popen([sys.executable] + sys.argv)

    # def clear_frame(self):
    #    if hasattr(self, "current_frame") and self.current_frame is not None:
    #        self.current_frame.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
