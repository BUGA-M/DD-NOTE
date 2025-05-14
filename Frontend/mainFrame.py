import customtkinter as ctk
from Custom import CreatScrollableFrame, CreateImage,CreatLabel, CreatFrame, FontInstaller, CreatButton, Places, CreateImage, ThemeControls, ThemeManager, ThemeColors, ChangeFrame #, ProfileManager
#from PIL import Image
import os
from pathlib import Path
from tkinter import messagebox
from Backend.models import EtudiantManager,CodeVerificationManager,OrientationOFPPT,Validation
from tkinter import TclError


class CreateInterfaceGenerale(CreatFrame):
    def __init__(self, master, Type,keyClient):
        self.__type = Type
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        self.__items_Admin = ["Reduire","Profil", "Mes validation", "Les acceptation", "Settings"]
        self.__items_Formateur = ["Reduire","Profil", "Ajoute Notes", "Ajoute Absences", "Ajoute Séance", "Contact", "Settings"]
        self.__items_Etudiant = ["Reduire","Profil", "Mes Notes", "Mes absences", "Contact", "Settings"]
        super().__init__(
            master,
            1300,
            610,
            "transparent",
            self.theme_data["button"], 
            15
        )
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.EtudiantManager=EtudiantManager()
        self.keyClient=keyClient
        self.Create_Header()
        self.show_Frame()
        master.minsize(1280,720)
          
        
    def show_Frame(self):
        self.FramePlaceResponsive( 0.5, 0.53,0.98, 0.91,"center" )
    
    @staticmethod
    def creat_Pics():
        base_path = Path("./Custom/pic").resolve()
        
        pics = {
            "Reduire": CreateImage(str(base_path / "reduce.png"), width=50, height=50),
            "Profil": CreateImage(str(base_path / "male_profile.png"), width=50, height=50),
            "Mes Notes": CreateImage(str(base_path / "notes.png"), width=50, height=50),
            "Mes absences": CreateImage(str(base_path / "warning.png"), width=50, height=50),
            "Contact": CreateImage(str(base_path / "contact.png"), width=50, height=50),
            "Settings": CreateImage(str(base_path / "setting.png"), width=50, height=50)
        }

        return pics
        
    def Create_Header(self):
        
        self.pathUser = Path("./Custom/pic/Stagaire.png").resolve()
        self.picUserRonde = CreateImage().make_circular(self.pathUser,75, 75)
        
        self.pathReduire = Path("./Custom/pic/reduce.png").resolve()
        self.picReduire = CreateImage(str(self.pathReduire), width=50, height=50)
        
        self.header_frame = CreatFrame(self, 1300, 100, "#2B2B2B", fg_color=self.theme_data["button"],corner_radius=15)
        self.header_frame.place_responsive_width(0.5, 0, 1.001,"n")
        
        #self.header_name = CreatLabel(self.header_frame,self.get_infoEtudaint(self.keyClient), 22, self.title_font)
        #self.header_name.LabelPlace(0.09, 0.5, "center")
        
        self.logout_header = CreatButton(self.header_frame, "Logout", 120, 40, fg_color=self.theme_data["title"],text_font=self.type_font[0], font_size=16, command =self.change_to_accueil)
        self.logout_header.buttonPlace(0.943, 0.45, "center")
        self.logout_header.place_right_full_height(padding_top=25, padding_bottom=25,x_offset=15)
                
        self.Image_Profile = CreatLabel(self.header_frame, self.get_infoEtudaint(self.keyClient), 34, self.title_font[0],image=self.picUserRonde,cursor="hand2",bg_color="transparent",compound="left")
        self.Image_Profile.place_left_full_height(x_offset=10)
        self.Image_Profile.bind("<Button-1>", self.buttonClicked)
        
        #self.header_frame.FramePlace(0.5, 0.1, "center")
        
        self.Create_Content()
        self.Creat_Left()
        
        
        self.header_line= CreatFrame(self, 1300, 2, "transparent", fg_color=self.theme_data["border"],corner_radius=0)
        self.header_line.place_responsive_width(rely=0, relwidth=1,padding_y=95,anchor="n")
    
    def buttonClicked(self,event=None):
        print("button Profile clicker")
        

    
    def Creat_Left(self):
        self.left_frame = CreatFrame(self, 250, 400, fg_color=self.theme_data["button"],corner_radius=0)
        
        self.left_frame.place_left_full_height(91,15)
        
        self.left_line= CreatFrame(self, 2, 2, "transparent", fg_color=self.theme_data["border"],corner_radius=0)
        self.left_line.place_left_full_height(95,0,250)
        self.__icons_Etudiant = self.creat_Pics()
        try :
            match self.__type.lower():
                case "admin":
                    for index, item in enumerate(self.__items_Admin):
                        self.btn = CreatButton(
                            self.left_frame,
                            item,
                            250,
                            50,
                            font_size=18,
                            fg_color=self.theme_data["button"],
                            hover_color=self.theme_data["button_hover"],
                            command=lambda item=item: self.handle_button_click(item),
                            corner_radius=0
                        )
                        self.btn.buttonPlace(0.5, 0.2 + index * 0.15)
                        
                case "formateur":
                    for index, item in enumerate(self.__items_Formateur):
                        self.btn = CreatButton(
                            self.left_frame,
                            item,
                            250,
                            50,
                            font_size=18,
                            fg_color=self.theme_data["button"],
                            hover_color=self.theme_data["button_hover"],
                            command=lambda item=item: self.handle_button_click(item),
                            corner_radius=0
                        )
                        self.btn.buttonPlace(0.5, 0.2 + index * 0.15)

                case "stagaire":
                    for index, item in enumerate(self.__items_Etudiant):
                        image_icon = self.__icons_Etudiant[item].as_ctk()
                        self.btn = CreatLabel(
                            self.left_frame,
                            item,
                            20,
                            self.type_font[0],
                            image=image_icon ,
                            cursor="hand2",
                            bg_color="transparent",
                            compound="left",
                            anchor="w",
                            padx=10
                        )
                        
                        # Placer le label
                        self.btn.FramePlaceResponsive(0.5, 0.2 + index * 0.12, relwidth=1, relheight=0.1)
                        
                        # Ajouter plusieurs événements bind
                        self.btn.bind("<Enter>", lambda event, btn=self.btn: self.on_hover_enter(event, btn))
                        self.btn.bind("<Leave>", lambda event, btn=self.btn: self.on_hover_leave(event, btn))

                        self.btn.bind("<Button-1>", lambda event, item=item: self.handle_button_click(event, item))
                case '':
                    print(f"Type Vide ")
        except Exception as e:
            print(f"[error CASE]: {e}")
        
    def handle_button_click(self,event, item=None):
        self.content_frame.destroy()
        if item == "Profil":
            self.Affiche_Profils()
        elif item == "Mes Notes":
            self.Affiche_Notes()
        elif item == "Mes absences":
            self.display_absences()
        elif item == "Mes validation":
            self.display_validations()
        elif item == "Les acceptation":
            self.display_acceptations()
        elif item == "Settings":
            self.display_Settings()
        elif item == "Ajoute Notes":
            self.add_notes()
        elif item == "Ajoute Absences":
            self.add_absences()
        elif item == "Ajoute Séance":
            self.add_seance()
        elif item == "Contact":
            self.display_contact()
 
    def Create_Content(self):
        self.content_frame = CreatFrame(self, 1, 500, fg_color=self.theme_data["button"],corner_radius=0)
        self.content_subtitle = CreatLabel(
            self.content_frame,
            text="Select an option from the navigation menu",
            font_size=18
        )
        self.content_frame.place_responsive(margin_left=252, margin_top=95,margin_bottom=15,margin_right=-1)
        self.content_subtitle.LabelPlace(0.5, 0.5, "center")
    
    def Affiche_Profils(self):
        print(f"profile pas encore cree")
    
    def Affiche_Notes(self):
        print(f"Notes pas encore cree")
    

    def display_absences(self):
        print(f"absences pas encore cree")

    def display_absences(self):
            print(f"absences pas encore cree")

    def display_contact(self):
        print(f"contact pas encore cree")   
            
    def display_Settings(self):
        print(f"Settings pas encore cree")   
        
    def display_validations(self):
        label = CreatLabel(self.content_frame, text="Affichage des validations (à implémenter)", font_size=18)
        label.LabelPlace(0.5, 0.5, "center")

    def display_acceptations(self):
        label = CreatLabel(self.content_frame, text="Affichage des acceptations (à implémenter)", font_size=18)
        label.LabelPlace(0.5, 0.5, "center")

    def add_notes(self):
            label = CreatLabel(self.content_frame, text="Ajout de notes (à implémenter)", font_size=18)
            label.LabelPlace(0.5, 0.5, "center")

    def add_absences(self):
        label = CreatLabel(self.content_frame, text="Ajout d'absences (à implémenter)", font_size=18)
        label.LabelPlace(0.5, 0.5, "center")

    def add_seance(self):
        label = CreatLabel(self.content_frame, text="Ajout de séance (à implémenter)", font_size=18)
        label.LabelPlace(0.5, 0.5, "center")
             
    
    def get_infoEtudaint(self,email):
        INFO = self.EtudiantManager.get_etudiant_by_email(email)
        if INFO :
            return f"   {INFO[1] } { INFO[2]}"
        

    def on_hover_enter(self, event, btn):
        btn.configure(fg_color=self.theme_data["button_hover"])  # Changer la couleur au survol
        # Si tu veux changer d'autres propriétés, fais-le ici, comme changer la police, etc.

    def on_hover_leave(self, event, btn):
        btn.configure(fg_color=self.theme_data["button"])
            
    def on_hover(self,event):
        # Change la couleur de fond ou ajoute un effet lors du survol
        self.reduire_btn.configure(fg_color=self.theme_data["button_hover"])

    def off_hover(self,event):
        # Restaure la couleur de fond initiale après que la souris quitte le label
        self.reduire_btn.configure(fg_color=self.theme_data["button"])
        
    def change_to_accueil(self):
        from Frontend.connexion import ConnexionFrame
        from Frontend.Siscrire import Apk
        self.destroy()
        manager=ChangeFrame(self.master)
        FrameSinscrire=[
            lambda parent:Apk(parent,"Enter your code","Enter your password","admin.csv","admin"),
            lambda parent:Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"),
            lambda parent:Apk(parent,"Enter your CIN","Enter your password","Formateur.csv","Formateur")
        ]
        manager.show_frame(lambda parent: ConnexionFrame(parent,FrameSinscrire))
            
        
        