import customtkinter as ctk

class CreatLabel(ctk.CTkLabel):
    def __init__(self, Fenetre, Text="Par defaut", Font_size=16,
                 text_font="Arial", text_color="white", bg_color="black", **kwargs):

        super().__init__(
            master=Fenetre,
            text=Text,
            font=(text_font, Font_size),
            text_color=text_color,
            bg_color=bg_color,
            **kwargs
        )

    # ➕ Méthodes utilitaires

    def LabelPack(self, padx=0, pady=0, **kwargs):
        self.pack(padx=padx, pady=pady, **kwargs)

    def LabelPlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def LabelGride(self, row=0, column=0, padx=0, pady=0, sticky="nsew", rw=1, cw=1, **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)

        if hasattr(self.master, "grid_rowconfigure"):
            self.master.grid_rowconfigure(row, weight=rw)
        if hasattr(self.master, "grid_columnconfigure"):
            self.master.grid_columnconfigure(column, weight=cw)

    def LabelConfig(self, **option):
        self.configure(**option)
