import customtkinter as ctk

class CreatOptionMenu(ctk.CTkOptionMenu):
    
    def __init__(self, fenetre, values=None, variable=None,
                 width:int=150, height:int=40,
                 text_font="Arial", font_size=12,
                 fg_color="black", text_color="white",
                 button_color="black", button_hover_color=None,
                 command=None, **kwargs):

        super().__init__(
            master=fenetre,
            values=values,
            variable=variable,
            width=width,
            height=height,
            font=(text_font, font_size),
            fg_color=fg_color,
            text_color=text_color,
            button_color=button_color,
            button_hover_color=button_hover_color,
            command=command,
            **kwargs
        )

    # ➕ Méthodes utilitaires

    def OptionMenuPack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def OptionMenuPlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def OptionMenuGrid(self, row=0, column=0, padx=0, pady=0, sticky="", **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)

    def OptionMenuConfig(self, **option):
        self.configure(**option)
