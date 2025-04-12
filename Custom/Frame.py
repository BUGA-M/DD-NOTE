import customtkinter as ctk

class CreatFrame(ctk.CTkFrame):
    def __init__(self, Fenetre, width, height, bg_color,
                 fg_color=None, corner_radius=15, border_width=0, border_color=None, **kwargs):

        super().__init__(
            master=Fenetre,
            width=width,
            height=height,
            bg_color=bg_color,
            fg_color=fg_color,
            corner_radius=corner_radius,
            border_color=border_color,
            border_width=border_width,
            **kwargs
        )

        # Rendre le contenu extensible en interne si on utilise grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # ➕ Méthodes utilitaires

    def FramePack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        """Pack le frame avec options de marge, expansion et remplissage"""
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def FramePlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        """Place le frame avec relx/rely et ancrage"""
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def FrameGride(self, row=0, column=0, padx=0, pady=0, sticky="nsew", **kwargs):
        """Grid le frame avec position, padding, et sticky pour expansion"""
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)
        # Activation de la responsivité côté parent si c’est un CTk-compatible
        if hasattr(self.master, "grid_rowconfigure"):
            self.master.grid_rowconfigure(row, weight=1)
            self.master.grid_columnconfigure(column, weight=1)

    def FrameConfig(self, **options):
        """Configurer dynamiquement le frame"""
        self.configure(**options)
