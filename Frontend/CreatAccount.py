import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import csv, re, random
import sqlite3
import smtplib
from email.message import EmailMessage
import ssl
from pathlib import Path
from datetime import datetime
from Frontend.ForgetPassword import ForgetPassword
from Custom import CreatLabel, CreatEntry, CreatButton, CreatFrame, CreatComboBox, CreatOptionMenu, FontInstaller, ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
from Frontend.Siscrire import Apk
from dotenv import load_dotenv
import sqlite3
import os
import hashlib
from datetime import datetime
from Backend.models import EtudiantManager,CodeVerificationManager,OrientationOFPPT,Validation
from Backend.config import NEW_ACC_KEY

class CreatAccount(CreatFrame):
    def __init__(self, master):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(
            master,
            550,
            550,
            "transparent",
            self.theme_data["button"], 
            20
        )
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")

        #self.basedonne=BaseDonnees()
        self.EtudiantManager=EtudiantManager()
        self.codeOTP=CodeVerificationManager()
        self.bac_var = tk.StringVar()

        self.sexe = ["Homme", "Femme"]
        self.niv_scolaire  = ["6éme année primaire", "3ème année collége", "Niveau Bac", "Baccalauréat"]
        self.ListBac = [
            "Sciences Mathématiques A",
            "Sciences Mathématiques B",
            "Sciences Physiques",
            "Sciences de la Vie et de la Terre",
            "Sciences Agronomiques",
            "Sciences et Technologies Électriques",
            "Sciences et Technologies Mécaniques",
            "Arts Appliqués",
            "Sciences Économiques",
            "Sciences de Gestion Comptable",
            "Lettres",
            "Sciences Humaines",
            "Sciences Islamiques",
            "2ème Bac Sciences Mathématiques A (BIOF)",
            "2ème Bac Sciences Mathématiques B (BIOF)",
            "2ème Bac Sciences Physiques (BIOF)",
            "2ème Bac Sciences de la Vie et de la Terre (SVT) (BIOF)",
            "2ème Bac Sciences Agronomiques (BIOF)",
            "2ème Bac Sciences et Technologies Électriques (BIOF)",
            "2ème Bac Sciences et Technologies Mécaniques (BIOF)"
        ]
        self.Validation_class = Validation()
        self.CreatInterface()
    
    def CreatInterface(self):
        self.pathReturn = Path("./Custom/pic/return.png").resolve()
        self.picReturn = CreateImage(str(self.pathReturn), width=20, height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_connecte,fg_color=self.theme_data["title"])
        self.returnButton.buttonPlace(0.07,0.07, "center")
        self.returnButton.buttonConfig(font=(self.type_font, 14, "bold"))

        self.LabelSinscrire = CreatLabel(self, "S'inscrire", 30, self.title_font, "white", "transparent")
        self.LabelSinscrire.LabelPlace(0.5, 0.09, "center")
        self.LabelSinscrire.LabelConfig(font=(self.title_font[0], 29, "bold"))
        self.ligne = CreatFrame(self, 485, 2, fg_color="#dfdddb")
        self.ligne.FramePlace(rely=0.16)

        self.subtitle = CreatLabel(self, "Bienvenue! Remplissez les champs",13,self.subtitle_font,"#B0B0B0")
        self.subtitle.LabelPlace(0.5, 0.19, "center")
        self.subtitle.LabelConfig(font=(self.subtitle, 13, "bold"))

        self.nom = CreatEntry(self, 235, 42, 7, 0, placeholder_text="Votre Nom *", Font_size=12)

        self.prenom = CreatEntry(self, 235, 42, 7, 0, placeholder_text="Votre Prenom *",Font_size=12)

        self.Sexe = CreatOptionMenu(
            master=self,
            values=self.sexe,
            width=235,
            height=42,
            fg_color="white",
            bg_color="transparent",
            text_color="#3E3E3E",
            corner_radius=7, 
            state="readonly",
            button_color=self.theme_data["button_hover"],
            dropdown_fg_color=self.theme_data["title"]
        )
        self.Sexe.set("Votre Sexe *")

        self.dateNaissance=CreatEntry(self,235,42,7,0,placeholder_text="Votre Date Naissance *",Font_size=12,text_color="#3E3E3E")

        self.Bac=CreatEntry(self,235,42,7,0,placeholder_text="Votre Année de bac *",Font_size=12)

        self.TypeBAC=CreatOptionMenu(self,self.ListBac,width=485,height=42,text_color="#3E3E3E",corner_radius=7, state="readonly",button_color=self.theme_data["button_hover"],command=self.bac_selectionner,dropdown_fg_color=self.theme_data["title"])
        self.TypeBAC.set("Pas de Bac")

        self.Niv_Scolaire = CreatOptionMenu(
            master=self,
            values=self.niv_scolaire,
            width=235,
            height=42,
            fg_color="white",
            bg_color="transparent",
            text_color="#3E3E3E",
            corner_radius=7,
            state="readonly",
            button_color=self.theme_data["button_hover"],
            dropdown_fg_color=self.theme_data["title"]
        )
        self.Niv_Scolaire.set("Votre Niveau scolaire *")

        self.Filiere = CreatOptionMenu(
            master=self,
            values=[],
            width=485,
            height=42,
            fg_color="white",
            bg_color="transparent",
            text_color="#3E3E3E",
            corner_radius=7,
            state="readonly",
            button_color=self.theme_data["button_hover"],
            dropdown_fg_color=self.theme_data["title"]
        )
        self.Filiere.set("Votre Filiéres *")

        self.Niv_Scolaire.update_options(command=lambda value: self.check_niveau())

        self.email=CreatEntry(self,485,42,7,0,placeholder_text="Votre Email *",Font_size=12,text_color="#3E3E3E")

        self.buttonConnect=CreatButton(self,"Valide",485,35,command=self.valide_formulaire,fg_color=self.theme_data["title"])
        self.buttonConnect.buttonConfig(font=(self.type_font,14,"bold"))

        self.ConnecteAccount=CreatButton(self,"Vous avez un compte ? Connectez-vous ici",text_color="#B0B0B0",hover_color="#2C3440",fg_color="transparent",corner_radius=7,height=30,command=self.change_to_connecte)
        self.ConnecteAccount.bind("<Enter>", self.on_entre)
        self.ConnecteAccount.bind("<Leave>", self.on_leave)
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="white",
            bg_color="transparent"
        )
        # enmplacement des widgets dans le frame
        self.Bac_Non_Selected()
        self.show_Frame()

    def Bac_Non_Selected(self):
        self.nom.EntryPlace(0.27, 0.29, "center")
        self.prenom.EntryPlace(0.73, 0.29, "center")
        self.Sexe.place_option_menu(0.27, 0.39, "center")
        self.dateNaissance.EntryPlace(0.73,0.39,"center")
        self.Bac.EntryPlace(0.27,0.49,"center")
        self.Niv_Scolaire.place_option_menu(0.73,0.49,"center")
        self.TypeBAC.place_option_menu(0.5,0.59,"center")
        self.Filiere.place_option_menu(0.5,0.59,"center")
        self.email.EntryPlace(0.5,0.69,"center")
        self.buttonConnect.buttonPlace(0.5,0.80,"center")
        self.ConnecteAccount.buttonPlace(0.5,0.87,"center")
        self.footer.LabelPlace(relx=0.5,rely=0.94,anchor="center")
        self.configure(height=550)
        self.TypeBAC.set("Pas de Bac")
        self.bac_var.set("Votre Année de bac *")
        self.Bac.configure(state="readonly")
        
    def Bac_Selected(self):
        self.nom.EntryPlace(0.27, 0.29, "center")
        self.prenom.EntryPlace(0.73, 0.29, "center")
        self.Sexe.place_option_menu(0.27, 0.38, "center")
        self.dateNaissance.EntryPlace(0.73,0.38,"center")
        self.Bac.EntryPlace(0.27,0.47,"center")
        self.Niv_Scolaire.place_option_menu(0.73,0.47,"center")
        self.TypeBAC.place_option_menu(0.5,0.56,"center")
        self.Filiere.place_option_menu(0.5,0.65,"center")
        self.email.EntryPlace(0.5,0.74,"center")
        self.buttonConnect.buttonPlace(0.5,0.84,"center")
        self.ConnecteAccount.buttonPlace(0.5,0.92,"center")
        self.footer.LabelPlace(relx=0.5,rely=0.97,anchor="center")
        self.configure(height=590)
        self.TypeBAC.set("Votre type de BAC")
        self.Bac.configure(state="normal")
        #self.bac_var.set("YYYY") 
        
    def bac_selectionner(self, selected_bac):
        if self.Niv_Scolaire.get() == "Baccalauréat":
            self.filières_ofppt = OrientationOFPPT.get_filiere_from_bac(selected_bac)
            self.Filiere.update_options(values=self.filières_ofppt)
            self.Filiere.set("Votre Filiéres *")
   
    def check_niveau(self):
        selected_niveau = self.Niv_Scolaire.get()
        
        if selected_niveau == "6éme année primaire":
            self.filières_ofppt = [
                "gestion hôtelière", "génie civil", "électromécanique", "mécanique",
                "électricité", "gestion", "tourisme", "btp (bâtiment et travaux publics)"
            ]
            self.Bac_Non_Selected()
        elif selected_niveau == "Baccalauréat":
            self.filières_ofppt =[]
            self.Bac_Selected()
        elif selected_niveau == "Niveau Bac":
            self.filières_ofppt = [
                "pâtisserie", "métiers de la coiffure et esthétique", 
                "plomberie sanitaire", "menuiserie aluminium et bois"
            ]
            self.Bac_Non_Selected()
        elif selected_niveau == "3ème année collége":
            self.filières_ofppt = [
                "pâtisserie", "métiers de la coiffure et esthétique", 
                "plomberie sanitaire", "menuiserie aluminium et bois"
            ]
            self.Bac_Non_Selected()
        else:
            self.filières_ofppt=[]
        
        self.Filiere.update_options(values=self.filières_ofppt)
        self.Filiere.set("Votre Filiéres *")



    def on_entre(self,event):
        self.ConnecteAccount.buttonConfig(text_color=self.theme_data["text"])
   
    def on_leave(self,event):
        self.ConnecteAccount.buttonConfig(text_color="#B0B0B0")
    
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
    
    #def change_to_connecte(self):
    #    self.destroy()
    #    manager=ChangeFrame(self.master)
    #   manager.show_frame(lambda parent: Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"))

    def change_to_connecte(self):
        from Frontend.Siscrire import Apk
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"))
        
    def change_to_accueil(self):
        from Frontend.connexion import ConnexionFrame
        self.destroy()
        manager=ChangeFrame(self.master)
        FrameSinscrire=[
            lambda parent:Apk(parent,"Enter your code","Enter your password","admin.csv","admin"),
            lambda parent:Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"),
            lambda parent:Apk(parent,"Enter your CIN","Enter your password","Formateur.csv","Formateur")
        ]
        manager.show_frame(lambda parent: ConnexionFrame(parent,FrameSinscrire))
    
    def valide_formulaire(self):
        try:
            nom = self.nom.get().strip()
            prenom = self.prenom.get().strip()
            email = self.email.get().strip().lower()
            dateNaissance = self.dateNaissance.get().strip()
            Niv_scolaire = self.Niv_Scolaire.get().strip()
            TypeBac = self.TypeBAC.get().strip()
            year_bac = self.Bac.get().strip()
            filiere = self.Filiere.get().strip()
            sexe = self.Sexe.get().strip()

            valide_nom = self.Validation_class.validate_nom_prenom(nom, "nom")
            valide_prenom = self.Validation_class.validate_nom_prenom(prenom, "prénom")
            valide_email = self.Validation_class.validate_email(email)
            valide_password = NEW_ACC_KEY
            valide_date_Naissance = self.Validation_class.validate_date_naissance(dateNaissance)
            valide_Niv_scolaire = self.Validation_class.validate_niveau_scolaire(Niv_scolaire)
            valide_TypeBac = self.Validation_class.validate_Typebac(TypeBac)
            valide_year_bac = self.Validation_class.validate_bac_year(year_bac) if valide_Niv_scolaire == "Baccalauréat" else "Null"
            valide_filiere = self.Validation_class.validate_filiere(filiere)
            valide_sexe = self.Validation_class.validate_sexe(sexe)
            

            all_valide = [valide_nom, valide_prenom, valide_email, valide_password,
                          valide_date_Naissance, valide_Niv_scolaire, valide_TypeBac,
                          valide_year_bac,valide_sexe,valide_filiere
                          ]

            if all(all_valide):
                self.EtudiantManager.supprimer_email_non_valide(email)
                if self.EtudiantManager.email_existe(email):
                    messagebox.showwarning("Adresse e-mail déjà utilisée",
                        "Cette adresse e-mail est déjà utilisée par un autre compte. Veuillez saisir une autre adresse e-mail, s'il vous plaît.")
                    return
                else:
                    messagebox.showinfo("Succès", "Inscription enregistrée. Veuillez vérifier votre email.")
                    self.EtudiantManager.inscrire_etudiant(
                        valide_nom, valide_prenom, valide_email, valide_password,
                        valide_date_Naissance, valide_Niv_scolaire, valide_TypeBac, valide_year_bac,
                        valide_filiere, valide_sexe
                    )
                    self.sendEmailCode(email)
                    self.change_to_otp(email)
        except Exception as e:
            print(f"Erreur: {e}")  
            messagebox.showerror("Erreur système", f"Une erreur inattendue s'est produite: {str(e)}")

    
    def change_to_otp(self,email):
        from Frontend.OTP_Email import OTP_Email
        self.destroy()
        manager = ChangeFrame(self.master)
        manager.show_frame(lambda parent: OTP_Email(parent, "Stagaire.csv", "Stagaire",email))

    def sendEmailCode(self, Email_receiver):
        load_dotenv()
        email_sender = str(os.getenv("EMAIL_SENDER"))
        email_password = str(os.getenv("EMAIL_PASSWORD"))
        email_receiver = Email_receiver

        Subject = "Vérification OTP de l'adresse e-mail - DD-NOTE"
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = Subject

        context = ssl.create_default_context()
        code = str(random.randint(100000,999999))

        html_content = f"""\
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Vérification OTP de l'adresse e-mail - DD-NOTE</title>
                <!--[if mso]>
                <style type="text/css">
                    table, td {{font-family: Arial, Helvetica, sans-serif;}}
                </style>
                <![endif]-->
            </head>
            <body style="margin:0; padding:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafb;">
                <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #f9fafb;">
                    <tr>
                        <td align="center" style="padding:20px 0;">
                            <table role="presentation" style="width:100%; max-width:650px; border-collapse: collapse; border:0; border-spacing:0; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);">
                                <!-- Header -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, {self.theme_data['title']}, {self.theme_data['button']}); padding: 30px 0; text-align: center; border-radius: 10px 10px 0 0;">
                                        <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0;">
                                            <tr>
                                                <td align="center">
                                                    <div style="background-color: #ffffff; width: 110px; height: 110px; border-radius: 55px; display: inline-block; margin-bottom: 20px;">
                                                        <a href="#" style="
                                                            display: inline-block;
                                                            width: 100%;
                                                            height: 100%;
                                                            border-radius: 55px;
                                                            text-align: center;
                                                            line-height: 110px;
                                                            color: #111827;
                                                            font-weight: bold;
                                                            font-size: 16px;
                                                            text-decoration: none;
                                                            background-color: rgba(255, 255, 255, 0.1);
                                                        ">
                                                            DD-NOTE
                                                        </a>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td align="center">
                                                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">Vérification de l'adresse e-mail via un code OTP</h1>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- Content -->
                                <tr>
                                    <td style="padding: 40px 30px; color: #374151;">
                                        <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0;">
                                            <tr>
                                                <td>
                                                    <p style="font-size: 18px; font-weight: 500; margin: 0 0 20px 0;">Bonjour,</p>
                                                    <p style="font-size: 16px; line-height: 24px; margin: 0 0 30px 0;">
                                                        Nous avons reçu une demande de création de compte pour votre adresse e-mail sur DD-NOTE.Pour assurer la sécurité de votre compte, veuillez utiliser le code de vérification ci-dessous
                                                    </p>
                                                </td>
                                            </tr>
                                            
                                            <!-- Code container -->
                                            <tr>
                                                <td style="padding: 20px 0;">
                                                    <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #f3f4f6; border-radius: 10px;">
                                                        <tr>
                                                            <td style="padding: 25px; text-align: center;">
                                                                <p style="margin: 0 0 15px 0; color: #6b7280; font-size: 16px; font-weight: 500;">Votre code de vérification :</p>
                                                                <div style="font-size: 32px; letter-spacing: 6px; color: {self.theme_data['title']}; font-weight: 700; margin: 15px 0; padding: 15px; background-color: #ffffff; border-radius: 10px; display: inline-block; min-width: 180px; border: 1px solid #e5e7eb;">{code}</div>
                                                                <p style="color: #6b7280; margin: 15px 0 0 0; font-size: 14px; font-weight: 500;">Valable pendant 5 minutes</p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                            
                                            <!-- Warning -->
                                            <tr>
                                                <td style="padding: 20px 0;">
                                                    <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #fff8e6; border-radius: 6px; border-left: 4px solid #fbbf24;">
                                                        <tr>
                                                            <td style="padding: 15px; display: flex;">
                                                                <table role="presentation" style="border-collapse: collapse; border:0; border-spacing:0;">
                                                                    <tr>
                                                                        <td width="30" style="vertical-align: top; padding-right: 15px;">
                                                                            <!-- Triangle Alert Icon (simplified) -->
                                                                            <div style="width: 24px; height: 24px; font-weight: bold; color: #d97706; text-align: center;">⚠️</div>
                                                                        </td>
                                                                        <td>
                                                                            <div style="font-weight: 500; color: #92400e; font-size: 15px; line-height: 22px;">
                                                                                Ne partagez jamais ce code avec qui que ce soit. Nos représentants ne vous demanderont jamais ce code.
                                                                            </div>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                            
                                            <!-- Contact info -->
                                            <tr>
                                                <td style="padding: 20px 0;">
                                                    <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #f3f4f6; border-radius: 10px;">
                                                        <tr>
                                                            <td style="padding: 25px;">
                                                                <h3 style="margin-top: 0; color: {self.theme_data['title']}; font-size: 18px; font-weight: 600; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid {self.theme_data['title']}; display: inline-block;">Support technique</h3>
                                                                <p style="font-size: 15px; line-height: 24px; margin: 0;">
                                                                    📧 ddnote.ma@gmail.com<br>
                                                                    📞 +212 6 66 66 66 66<br>
                                                                    🏢 OFPPT - Dévelopement Digital
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: {self.theme_data['title']}; color: #e5e7eb; padding: 30px; text-align: center; border-radius: 0 0 10px 10px;">
                                        <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0;">
                                            <!-- Social Links -->
                                            <tr>
                                                <td align="center" style="padding: 0 0 20px 0;">
                                                    <table role="presentation" style="border-collapse: collapse; border:0; border-spacing:0;">
                                                        <tr>
                                                            <td style="padding: 0 10px;">
                                                                <a href="#" style="
                                                                    display: inline-block;
                                                                    background-color: rgba(255, 255, 255, 0.1);
                                                                    width: 36px;
                                                                    height: 36px;
                                                                    border-radius: 18px;
                                                                    text-align: center;
                                                                    line-height: 36px;
                                                                    color: white;
                                                                    font-weight: bold;
                                                                    font-size: 16px;
                                                                    text-decoration: none;
                                                                ">
                                                                    F
                                                                </a>
                                                            </td>
                                                            <td style="padding: 0 10px;">
                                                                <a href="#" style="
                                                                    display: inline-block;
                                                                    background-color: rgba(255, 255, 255, 0.1);
                                                                    width: 36px;
                                                                    height: 36px;
                                                                    border-radius: 18px;
                                                                    text-align: center;
                                                                    line-height: 36px;
                                                                    color: white;
                                                                    font-weight: bold;
                                                                    font-size: 16px;
                                                                    text-decoration: none;
                                                                ">
                                                                    G
                                                                </a>
                                                            </td>
                                                            <td style="padding: 0 10px;">
                                                                <a href="#" style="
                                                                    display: inline-block;
                                                                    background-color: rgba(255, 255, 255, 0.1);
                                                                    width: 36px;
                                                                    height: 36px;
                                                                    border-radius: 18px;
                                                                    text-align: center;
                                                                    line-height: 36px;
                                                                    color: white;
                                                                    font-weight: bold;
                                                                    font-size: 16px;
                                                                    text-decoration: none;
                                                                ">
                                                                    X
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                            
                                            <!-- Divider -->
                                            <tr>
                                                <td align="center" style="padding: 0 0 20px 0;">
                                                    <div style="height: 1px; background-color: black; width: 80%;"></div>
                                                </td>
                                            </tr>
                                            
                                            <!-- Copyright -->
                                            <tr>
                                                <td align="center">
                                                    <p style="margin: 0; color: white; font-size: 14px;">© 2025 DD-NOTE. Tous droits réservés.</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
        """

        # Version texte simple pour les clients email qui ne supportent pas HTML
        text_content = f"""\
            Réinitialisation de mot de passe DD-NOTE-OFPPT

            Bonjour,

            Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte.
            Votre code de vérification est : {code}
            Ce code est valable pendant 5 minutes.

            Ne partagez jamais ce code avec qui que ce soit.

            Cordialement,
            L'équipe DD-NOTE-OFPPT
        """

        # Ajouter les deux versions au message
        em.set_content(text_content)
        em.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.send_message(em)

            if self.codeOTP.enregistrer_code(Email_receiver,code):
                messagebox.showinfo("Succès", "Le code de vérification a été envoyé à votre adresse e-mail avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {str(e)}")