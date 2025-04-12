import customtkinter as ctk

class CreatButton(ctk.CTkButton):
    def __init__(self, fenter, text, width, height,
                 command=None, corner_radius=12,
                 fg_color="blue", hover_color="darkblue",
                 border_width=0, border_color=None,
                 text_color="white", text_font="Arial", font_size=12, **kwargs):

        super().__init__(
            master=fenter,
            text=text,
            width=width,
            height=height,
            command=command,
            corner_radius=corner_radius,
            fg_color=fg_color,
            hover_color=hover_color,
            border_width=border_width,
            border_color=border_color,
            text_color=text_color,
            font=(text_font, font_size),
            **kwargs
        )

    # ➕ Méthodes utilitaires

    def buttonPack(self, padx=0, pady=0, **kwargs):
        self.pack(padx=padx, pady=pady, **kwargs)

    def buttonPlace(self, relx=0.5, rely=0.5, anchor="center", **kwargs):
        self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def ButtonGride(self, row=0, column=0, padx=0, pady=0, sticky="nsew", rw=1, cw=1, **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)
        
        if hasattr(self.master, "grid_rowconfigure"):
            self.master.grid_rowconfigure(row, weight=rw)
        if hasattr(self.master, "grid_columnconfigure"):
            self.master.grid_columnconfigure(column, weight=cw)

    def buttonConfig(self, **option):
        self.configure(**option)
