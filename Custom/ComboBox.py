import customtkinter as ctk

class CreatComboBox(ctk.CTkComboBox):
    def __init__(self, fenetre, value=value(), width, height,
                 text_font="Arial", font_size=12, state="normal",
                 fg_color="black", bg_color="black",
                 dropdown_text_color=None, button_color=None, **kwargs):

        super().__init__(
            master=fenetre,
            values=value,
            width=width,
            height=height,
            font=(text_font, font_size),
            state=state,
            fg_color=fg_color,
            bg_color=bg_color,
            dropdown_text_color=dropdown_text_color,
            button_color=button_color,
            **kwargs
        )

    # ➕ Méthodes utilitaires
    def value():
        return ['marouane','abdellah','youssef','imad']

    def ComboBoxPack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

    def ComboBoxPlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def ComboxGride(self, row=0, column=0, padx=0, pady=0, sticky="", **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)

    def ComboBoxConfig(self, **option):
        self.configure(**option)
