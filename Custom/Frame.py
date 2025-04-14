import customtkinter as ctk

class CreatFrame(ctk.CTkFrame):
    def __init__(self, Fenetre, width:int==300, height:int=300, bg_color,
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # ➕ Méthodes utilitaires

    def FramePack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def FramePlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def FrameGride(self, row=0, column=0, padx=0, pady=0, sticky="nsew", rw=1, cw=1, **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)
        
        if hasattr(self.master, "grid_rowconfigure"):
            self.master.grid_rowconfigure(row, weight=rw)
        if hasattr(self.master, "grid_columnconfigure"):
            self.master.grid_columnconfigure(column, weight=cw)

    def FrameConfig(self, **options):
        self.configure(**options)
