import customtkinter as ctk

class CreatEntry(ctk.CTkEntry):
    def __init__(self, Fenetre, width:int=100, height:int=50,
                 corner_radius=12, border_width=0,
                 fg_color="white", border_color=None,
                 text_color="black", Font_size=16,
                 text_font="Arial", placeholder_text="Entrez votre texte...", **kwargs):

        super().__init__(
            master=Fenetre,
            width=width,
            height=height,
            border_width=border_width,
            fg_color=fg_color,
            border_color=border_color,
            text_color=text_color,
            font=(text_font, Font_size),
            corner_radius=corner_radius,
            placeholder_text=placeholder_text,
            **kwargs
        )

    # ➕ Méthodes utilitaires

    def EntryPack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def EntryPlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def EntryGride(self, row=0, column=0, padx=0, pady=0, sticky="", **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)

    def EntryConfig(self, **option):
        self.configure(**option)
