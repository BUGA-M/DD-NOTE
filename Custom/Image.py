import customtkinter as ctk
import os
from pathlib import Path
from PIL import Image, ImageTk


class CreateImage(ctk.CTkImage):
    def __init__(self, path: str = None, lightPath: str = None, darkPath: str = None, width: int = 100, height: int = 100):
        self.defaultImage = Path("../DDnote/Custom/pic/default-IMG.png").resolve()

        self.path = path if path else self.defaultImage
        self.lightPath = lightPath if lightPath else self.path
        self.darkPath = darkPath if darkPath else self.path

        for imgPath in [self.path, self.lightPath, self.darkPath]:
            if imgPath and not os.path.exists(imgPath):
                raise FileNotFoundError(f"Le fichier image '{imgPath}' n'existe pas.")

        super().__init__(
            light_image=Image.open(self.lightPath),
            dark_image=Image.open(self.darkPath),
            size=(width, height)
        )

        self.ico_image = None
        try:
            img = Image.open(self.path)
            img = img.resize((32, 32))
            self.ico_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Warning: Impossible de créer l'icône de fenêtre: {e}")
            
            
    def resize(self, width, height):
        light = Image.open(self.lightPath).resize((width, height), Image.LANCZOS)
        dark = Image.open(self.darkPath).resize((width, height), Image.LANCZOS)
        self.configure(light_image=light, dark_image=dark, size=(width, height))


    def as_ctk(self):
        return self

    def as_icon(self):
        return self.ico_image
