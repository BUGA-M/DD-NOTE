import customtkinter as ctk
from Custom import CreatLabel, CreatFrame, FontInstaller

class ConnexionFrame(CreatFrame):
    def __init__(self, master):
        super().__init__(
            Fenetre=master,
            width=600,
            height=400,
            bg_color="transparent",
            fg_color="#2c3e50",
            corner_radius=15
        )

        # Utilisation de la font Orbiton
        font1 = FontInstaller.get_font("Orbiton", 20)

        self.labelTitle = CreatLabel(
            self,
            Text="LoGo",
            Font_size=font1[1],
            text_font=font1[0],
            bg_color="transparent"
        )
        self.labelTitle.LabelPack(pady=100)

    def show(self):
        self.FrameGride(padx=10, pady=10)


    