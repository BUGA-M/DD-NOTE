import customtkinter as ctk

class CreatOptionMenu(ctk.CTkOptionMenu):
    """
    Menu déroulant personnalisé basé sur CTkOptionMenu de CustomTkinter.
    Permet de configurer plus facilement le style, les dimensions et le comportement.
    """

    def __init__(
        self,
        master,
        values=None,
        variable=None,
        width: int = 150,
        height: int = 40,
        font_family: str = "Arial",
        font_size: int = 12,
        fg_color: str = "white",
        text_color: str = "black",
        button_color: str = "black",
        button_hover_color: str = None,
        command=None,
        **kwargs
    ):
        super().__init__(
            master=master,
            values=values,
            variable=variable,
            width=width,
            height=height,
            font=(font_family, font_size),
            fg_color=fg_color,
            text_color=text_color,
            button_color=button_color,
            button_hover_color=button_hover_color,
            command=command,
            **kwargs
        )

    # Méthodes d'affichage pratiques
    def pack_option_menu(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def place_option_menu(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def grid_option_menu(self, row=0, column=0, padx=0, pady=0, sticky="", **kwargs):
        
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)

    def update_options(self, **options):
        
        self.configure(**options)
