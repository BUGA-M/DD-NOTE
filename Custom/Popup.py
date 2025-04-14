import customtkinter as ctk
from Les_modules.Label import CreatLabel
from Les_modules.Button import CreatButton
from Les_modules.Entry import CreatEntry
from Les_modules.image import CreateImage
import os
from pathlib import Path

class CreatPopup(ctk.CTkToplevel):
    def __init__(self, window, title='new popup', width=400, height=120, **kwargs):
        if window is None:
            raise ValueError("Le paramètre 'window' ne peut pas être None. Passe une fenêtre principale.")

        super().__init__(window)

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()

        self._bg_color = kwargs.get("fg_color", "#000000")
        self.configure(fg_color=self._bg_color)

        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_label(self, padx=5, pady=5, fill='both', expand=True, **kwargs):
        label = CreatLabel(self.mainFrame, **kwargs)
        label.LabelPack(padx, pady, fill, expand)
        return label

    def add_button(self, padx=5, pady=5, fill='both', expand=True, command=None, **kwargs):
        button = CreatButton(self.mainFrame, command=lambda: self.CommandButton(command), **kwargs)
        button.buttonPack(padx, pady, fill, expand)
        return button

    def CommandButton(self, command):
        if command:
            command()
        self.ClosePopup()

    def ClosePopup(self):
        self.grab_release()
        self.destroy()

    def add_entry(self, padx=5, pady=5, fill='both', expand=True, **kwargs):
        entry = CreatEntry(self.mainFrame, **kwargs)
        entry.EntryPack(padx, pady, fill, expand)
        return entry

    def add_icon(self, **kwargs):
        icon = kwargs.get("path", None)
        if icon and os.path.exists(icon):
            photo = CreateImage(path=icon,width=32, height=32)
            self.photo = photo.get_ico_image()
            self.iconphoto(True, self.photo )
        else:
            raise ValueError("Le chemin de l'icône n'est pas fourni.")

    def WarningPopup(self, message:str='Ceci est un avertissement'):
        self.add_label(text=message, text_color="#FF0000")
        self.add_button(text="OK", fg_color="#FF5555", hover_color="#FF0000", command=self.ClosePopup)
        self.path=Path("../massar/Les_modules/pic/warning.ico").resolve()
        self.add_icon(path=self.path)

    def InfoPopup(self, message='Ceci est une information à savoir'):
        self.add_label(text=message, text_color="#2FA572")
        self.add_button(text="Fermer", fg_color="#2FA572", hover_color="#1E7A5E", command=self.ClosePopup)
        self.path=Path("../massar/Les_modules/pic/info.png").resolve()
        self.add_icon(path=self.path)

    def PopupConfig(self, **options):
        self.configure(**options)

    def get_Popup(self):
        return self
