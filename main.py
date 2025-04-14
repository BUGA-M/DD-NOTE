import customtkinter as ctk
from Frontend import ConnexionFrame
from Custom import FontInstaller
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.install_fonts()
        self.load_frames()

    def setup_window(self):
        self.geometry("1280x720")
        self.minsize(600, 720)
        self.title("DDnote")
        self.config(bg="#1e293b")

    def install_fonts(self):
        FontInstaller.installerFont("Titan One", "Custom/db_fonts/TitanOne-Regular.ttf", 50)
        FontInstaller.installerFont("Poppins", "Custom/db_fonts/Poppins-Regular.ttf", 22)

    def load_frames(self):
        self.connexion_frame = ConnexionFrame(self)
        self.connexion_frame.show()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
