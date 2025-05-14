import customtkinter as ctk
from .Position import Places

class CreatFrame(ctk.CTkFrame,Places):
    def __init__(self, Fenetre, width:int=300, height:int=300, bg_color='transparent',
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

    def FramePlace(self, relx=None, rely=None, anchor=None, **kwargs):
        if relx is None and rely is None and anchor is None:
            self.PlaceCenter(**kwargs)
        else:
            relx = relx if relx is not None else 0.5
            rely = rely if rely is not None else 0.5
            anchor = anchor if anchor is not None else "center"
            self.place(relx=relx, rely=rely, anchor=anchor, **kwargs)

    def FrameGride(self, row=0, column=0, padx=0, pady=0, sticky="nsew", rw=1, cw=1, **kwargs):
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, **kwargs)
        
        if hasattr(self.master, "grid_rowconfigure"):
            self.master.grid_rowconfigure(row, weight=rw)
        if hasattr(self.master, "grid_columnconfigure"):
            self.master.grid_columnconfigure(column, weight=cw)
 
    
    def FrameConfig(self, **options):
        self.configure(**options)
           
                     
    def FramePlaceResponsive(self, relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center", **kwargs):
        """
        Permet une flexibilité en hauteur et largeur (clean et simple pour les containers)
        """
        def update_place(event=None):
            # Vérifier si le widget existe toujours
            if self.winfo_exists():
                self.place(
                    relx=relx, 
                    rely=rely, 
                    relwidth=relwidth, 
                    relheight=relheight, 
                    anchor=anchor,
                    **kwargs
                )
        
        # Empêcher plusieurs bindings si déjà existant
        if hasattr(self, "_place_binding_id"):
            try:
                self.master.unbind("<Configure>", self._place_binding_id)
            except:
                pass
        
        # Vérifier si le master existe toujours
        if self.master and self.master.winfo_exists():
            # Lier le redimensionnement du parent
            self._place_binding_id = self.master.bind("<Configure>", update_place)
            update_place()
    
    
    def place_responsive(self, margin_left=0, margin_top=0, margin_right=0, margin_bottom=0,
                            relwidth=1, relheight=1, anchor="nw", 
                            min_width=None, min_height=None, 
                            max_width=None, max_height=None, **kwargs):
        """
        Meme que {FramePlaceResponsive} mais il t'offre des marges sur les quatre côtés.
        """
        def update_place(event=None):
            # Vérifier si le widget existe toujours
            try:
                if not self.winfo_exists():
                    return
                
                parent = self.master
                # Vérifier si le parent existe toujours
                if not parent.winfo_exists():
                    return
                    
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
            except (TclError, KeyError, AttributeError):
                # Si une exception se produit (widget détruit), supprimer le binding
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass
        
        # Gestion des bindings
        binding_attr = "_place_margin_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        # Créer un nouveau binding
        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        # S'assurer de supprimer le binding lorsque le widget est détruit
        self.bind("<Destroy>", on_destroy)
        
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
            # Vérifier si le widget existe toujours
            try:
                if not self.winfo_exists():
                    return
                    
                parent = self.master
                if not parent.winfo_exists():
                    return
                    
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
                
                parent_height = parent.winfo_height()
                if parent_height > 1 and (padding_top > 0 or padding_bottom > 0):
                    
                    rel_top = padding_top / parent_height if padding_top > 0 else 0
                    rel_bottom = padding_bottom / parent_height if padding_bottom > 0 else 0
                    
                    place_args['relheight'] = 1.0 - rel_top - rel_bottom

                safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'height']}
                place_args.update(safe_kwargs)
                
                self.place(**place_args)
            except (TclError, KeyError, AttributeError):
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass
        
        binding_attr = "_place_left_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        self.bind("<Destroy>", on_destroy)
        
        update_place()
        
        return self

    def place_right_full_height(self, padding_top=0, padding_bottom=0, x_offset=0, **kwargs):
        """
        Place le widget à droite de son parent avec une hauteur adaptative et des marges
        en haut et en bas. La largeur doit être définie à la création du widget.
        """
        def update_place(event=None):
            try:
                if not self.winfo_exists():
                    return
                    
                parent = self.master
                if not parent.winfo_exists():
                    return
                    
                parent_width = parent.winfo_width()
                parent_height = parent.winfo_height()

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
            except (TclError, KeyError, AttributeError):
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass

        binding_attr = "_place_right_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        self.bind("<Destroy>", on_destroy)

        update_place()

        return self

    def place_bottom_full_width(self, padding_left=0, padding_right=0, y_offset=0, height=None, **kwargs):
        """
        Place le widget en bas du parent avec une largeur adaptative.
        La hauteur peut être fixée via `height`. 
        Les paddings gauche/droite sont également pris en compte.
        """
        def update_place(event=None):
            try:
                if not self.winfo_exists():
                    return
                    
                parent = self.master
                if not parent.winfo_exists():
                    return
                    
                parent_width = parent.winfo_width()
                parent_height = parent.winfo_height()

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
            except (TclError, KeyError, AttributeError):
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass

        binding_attr = "_place_bottom_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        self.bind("<Destroy>", on_destroy)

        update_place()

        return self

    def place_top_full_width(self, padding_left=0, padding_right=0, y_offset=0, height=None, **kwargs):
        """
        Place le widget en haut du parent avec une largeur adaptative.
        La hauteur peut être fixée via `height`.
        Les paddings gauche/droite sont également pris en compte.
        """
        def update_place(event=None):
            try:
                if not self.winfo_exists():
                    return
                    
                parent = self.master
                if not parent.winfo_exists():
                    return
                    
                parent_width = parent.winfo_width()
                parent_height = parent.winfo_height()

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
            except (TclError, KeyError, AttributeError):
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass

        binding_attr = "_place_top_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        self.bind("<Destroy>", on_destroy)

        update_place()

        return self


    def place_responsive_width(self, relx=0.5, rely=0.5, relwidth=0.95, anchor="center", padding_x=0, padding_y=0, **kwargs):
        """
        Place le widget avec une largeur responsive par rapport à son parent.
        et block le frame en haut du parent avec {anchor="n"}
        """
        def update_place(event=None):
            try:
                if not self.winfo_exists():
                    return
                    
                parent = self.master
                if not parent.winfo_exists():
                    return
                    
                place_args = {
                    'relx': relx,
                    'rely': rely,
                    'relwidth': relwidth,
                    'anchor': anchor
                }
                
                if padding_x != 0:
                    place_args['x'] = padding_x
                
                if padding_y != 0:
                    place_args['y'] = padding_y
                
                safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['width', 'height']}
                place_args.update(safe_kwargs)
                
                # Placer le widget
                self.place(**place_args)
            except (TclError, KeyError, AttributeError):
                try:
                    self.master.unbind("<Configure>", getattr(self, binding_attr))
                except:
                    pass
        
        binding_attr = "_place_responsive_binding"
        if hasattr(self, binding_attr):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass

        setattr(self, binding_attr, self.master.bind("<Configure>", update_place))
        
        # Ajouter un binding pour nettoyer lorsque le widget est détruit
        def on_destroy(event):
            try:
                self.master.unbind("<Configure>", getattr(self, binding_attr))
            except:
                pass
        
        self.bind("<Destroy>", on_destroy)
        
        update_place()
        
        return self
