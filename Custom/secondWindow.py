import customtkinter as ctk
from Les_modules.Label import CreatLabel
from Les_modules.Button import CreatButton
from Les_modules.Entry import CreatEntry
from Les_modules.image import CreateImage
import os
from pathlib import Path
class CreateWindow(ctk.CTk):
    def __init__(self, window, title:str='SecondWindow', width:str=400, height:str=300,):

        if window is None:
            raise ValueError("Le paramètre 'window' ne peut pas être None. Passe une fenêtre principale.")

        super().__init__()
        self.window = window
        self.title(title)
        self.geometry("400x300")
        self.resizable(False,False)

        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def on_secondary_close():
        global secondary_window
        CreateWindow().attributes("-disabled", False)

        # Délai pour laisser finir les animations
        if secondary_window.winfo_exists():
            secondary_window.after(100, secondary_window.destroy)
        secondary_window = None

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
            photo = CreateImage(path=icon, width=32, height=32)
            self.photo = photo.get_ico_image()
            self.iconphoto(True, self.photo)
        else:
            raise ValueError("Le chemin de l'icône n'est pas fourni.")