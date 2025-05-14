import customtkinter as ctk

class CreatButton(ctk.CTkButton):
    def __init__(self, fenter, text:str='new BUTTON',width:int=100, height:int=20,
                 command=None, corner_radius=12,
                 fg_color="blue", hover_color="black",
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

    def buttonPack(self, padx=0, pady=0, fill="both", expand=True, **kwargs):
        self.pack(padx=padx, pady=pady, fill=fill, expand=expand, **kwargs)

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
        
    def place_responsive(self, margin_left=0, margin_top=0, margin_right=0, margin_bottom=0,
                        relwidth=1, relheight=1, anchor="nw", 
                        min_width=None, min_height=None, 
                        max_width=None, max_height=None, **kwargs):
        """
        Meme que {FramePlaceResponsive} mais il t'offre des marges sur les quatre côtés.
        """
        def update_place(event=None):
            parent = self.master
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            
            # Configuration de base - ancrage en haut à gauche
            place_args = {
                'relx': 0,
                'rely': 0,
                'x': margin_left,
                'y': margin_top,
                'anchor': anchor
            }
            
            # Seulement si le parent a une taille valide
            if parent_width > 1 and parent_height > 1:
                # Calculer la largeur et hauteur relatives pour tenir compte des marges
                total_horizontal_margin = margin_left + margin_right
                total_vertical_margin = margin_top + margin_bottom
                
                # Calculer les dimensions relatives ajustées
                if total_horizontal_margin > 0:
                    relative_margin_width = total_horizontal_margin / parent_width
                    adjusted_relwidth = relwidth - relative_margin_width
                    place_args['relwidth'] = max(0.01, adjusted_relwidth)  # Éviter les valeurs négatives
                else:
                    place_args['relwidth'] = relwidth
                
                if total_vertical_margin > 0:
                    relative_margin_height = total_vertical_margin / parent_height
                    adjusted_relheight = relheight - relative_margin_height
                    place_args['relheight'] = max(0.01, adjusted_relheight)  # Éviter les valeurs négatives
                else:
                    place_args['relheight'] = relheight
                
                # Calculer les dimensions effectives
                calculated_width = parent_width * place_args['relwidth']
                calculated_height = parent_height * place_args['relheight']
                
                # Appliquer les contraintes min/max
                if min_width is not None and calculated_width < min_width:
                    place_args['relwidth'] = min_width / parent_width
                
                if max_width is not None and calculated_width > max_width:
                    place_args['relwidth'] = max_width / parent_width
                
                if min_height is not None and calculated_height < min_height:
                    place_args['relheight'] = min_height / parent_height
                
                if max_height is not None and calculated_height > max_height:
                    place_args['relheight'] = max_height / parent_height
            else:
                # Si le parent n'a pas encore de dimensions valides, utiliser les valeurs par défaut
                place_args['relwidth'] = relwidth
                place_args['relheight'] = relheight
            
            # Ajouter les autres paramètres sécurisés
            safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'height']}
            place_args.update(safe_kwargs)
            
            # Placer le widget
            self.place(**place_args)
        
        # Gestion des bindings
        binding_attr = "_place_margin_binding"
        if hasattr(self, binding_attr):
            self.master.unbind("<Configure>", getattr(self, binding_attr))
        
        # Créer un nouveau binding
        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Placement initial
        update_place()
        
        # Retourner self pour permettre le chaînage
        return self
    
    def place_left_full_height(self, padding_top=0, padding_bottom=0, x_offset=0, **kwargs):
        """
        Place le widget à gauche de son parent avec une hauteur adaptative et des marges en
        haut et bas. La largeur doit être définie à la création du widget.
        """
        def update_place(event=None):
            place_args = {
                'relx': 0.0,       
                'rely': 0.0,      
                'anchor': "nw",    
                'relheight': 1.0,
            }
            
            if padding_top != 0:
                place_args['y'] = padding_top
            
            if x_offset != 0: 
                place_args['x'] = x_offset
            
            parent_height = self.master.winfo_height()
            if parent_height > 1 and (padding_top > 0 or padding_bottom > 0):
                
                rel_top = padding_top / parent_height if padding_top > 0 else 0
                rel_bottom = padding_bottom / parent_height if padding_bottom > 0 else 0
                
                place_args['relheight'] = 1.0 - rel_top - rel_bottom

            safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'height']}
            place_args.update(safe_kwargs)
            
            self.place(**place_args)
        
        binding_attr = "_place_left_binding"
        if hasattr(self, binding_attr):
            self.master.unbind("<Configure>", getattr(self, binding_attr))

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        update_place()
        
        return self

    def place_right_full_height(self, padding_top=0, padding_bottom=0, x_offset=0, **kwargs):
        """
        Place le widget à droite de son parent avec une hauteur adaptative et des marges
        en haut et en bas. La largeur doit être définie à la création du widget.
        """
        def update_place(event=None):
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()

            place_args = {
                'relx': 1.0,       # À droite
                'rely': 0.0,       # En haut
                'anchor': "ne",    # Ancre en haut à droite
                'relheight': 1.0,
            }

            if x_offset != 0:
                place_args['x'] = -x_offset  # Négatif car depuis la droite

            if parent_height > 1 and (padding_top > 0 or padding_bottom > 0):
                rel_top = padding_top / parent_height if padding_top > 0 else 0
                rel_bottom = padding_bottom / parent_height if padding_bottom > 0 else 0
                place_args['relheight'] = 1.0 - rel_top - rel_bottom
                if padding_top > 0:
                    place_args['y'] = padding_top

            safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'height']}
            place_args.update(safe_kwargs)

            self.place(**place_args)

        binding_attr = "_place_right_binding"
        if hasattr(self, binding_attr):
            self.master.unbind("<Configure>", getattr(self, binding_attr))

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))

        update_place()

        return self

    def place_bottom_full_width(self, padding_left=0, padding_right=0, y_offset=0, height=None, **kwargs):
        """
        Place le widget en bas du parent avec une largeur adaptative.
        La hauteur peut être fixée via `height`. 
        Les paddings gauche/droite sont également pris en compte.
        """
        def update_place(event=None):
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()

            place_args = {
                'relx': 0.0,
                'rely': 1.0,       # bas
                'anchor': "sw",    # ancre bas-gauche
                'relwidth': 1.0,
            }

            if y_offset != 0:
                place_args['y'] = -y_offset  # déplacement vers le haut

            # Si paddings horizontaux sont spécifiés
            if parent_width > 1 and (padding_left > 0 or padding_right > 0):
                rel_left = padding_left / parent_width if padding_left > 0 else 0
                rel_right = padding_right / parent_width if padding_right > 0 else 0
                place_args['relx'] = rel_left
                place_args['relwidth'] = 1.0 - rel_left - rel_right

            # Hauteur fixe si définie
            if height is not None:
                place_args['height'] = height

            safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'relheight']}
            place_args.update(safe_kwargs)

            self.place(**place_args)

        binding_attr = "_place_bottom_binding"
        if hasattr(self, binding_attr):
            self.master.unbind("<Configure>", getattr(self, binding_attr))

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))

        update_place()

        return self

    def place_top_full_width(self, padding_left=0, padding_right=0, y_offset=0, height=None, **kwargs):
        """
        Place le widget en haut du parent avec une largeur adaptative.
        La hauteur peut être fixée via `height`.
        Les paddings gauche/droite sont également pris en compte.
        """
        def update_place(event=None):
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()

            place_args = {
                'relx': 0.0,
                'rely': 0.0,       # en haut
                'anchor': "nw",    # ancre en haut à gauche
                'relwidth': 1.0,
            }

            if y_offset != 0:
                place_args['y'] = y_offset

            if parent_width > 1 and (padding_left > 0 or padding_right > 0):
                rel_left = padding_left / parent_width if padding_left > 0 else 0
                rel_right = padding_right / parent_width if padding_right > 0 else 0
                place_args['relx'] = rel_left
                place_args['relwidth'] = 1.0 - rel_left - rel_right

            if height is not None:
                place_args['height'] = height

            safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'relheight']}
            place_args.update(safe_kwargs)

            self.place(**place_args)

        binding_attr = "_place_top_binding"
        if hasattr(self, binding_attr):
            self.master.unbind("<Configure>", getattr(self, binding_attr))

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))

        update_place()

        return self
