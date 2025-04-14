import customtkinter as ctk
import os
from pathlib import Path
from PIL import Image, ImageTk

class CreateImage:
    def __init__(self, path:str=None, lightPath: str = None, darkPath: str = None, width: int = 100, height: int = 100):

        self.defaultImage = Path("../massar/Les_modules/pic/default-IMG.png").resolve()
        self.path = path if path else self.defaultImage
        self.lightPath = lightPath if lightPath else self.path
        self.darkPath = darkPath if darkPath else self.path
        self.width = width
        self.height = height

        for imgPath in [path,lightPath, darkPath]:
            if imgPath and not os.path.exists(imgPath):
                raise FileNotFoundError(f"Le fichier image '{imgPath}' n'existe pas.")

        self.image = ctk.CTkImage(
            light_image=Image.open(self.lightPath),
            dark_image=Image.open(self.darkPath),
            size=(self.width, self.height)
        )

        self.icoImage = None
        try:
            img = Image.open(self.path)
            img = img.resize((32, 32))
            self.icoImage = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Warning: Impossible de créer l'icône de fenêtre: {e}")

    def get_image(self):
        return self.image

    def get_ico_image(self):
        return self.icoImage