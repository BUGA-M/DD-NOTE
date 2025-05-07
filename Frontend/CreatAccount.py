import customtkinter as ctk
from tkinter import messagebox
import csv, re, random
import sqlite3
import smtplib
from email.message import EmailMessage
import ssl
from pathlib import Path
from datetime import datetime
from Frontend.ForgetPassword import ForgetPassword
from Custom import CreatLabel, CreatEntry, CreatButton, CreatFrame, CreatComboBox, FontInstaller, ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors,BaseDonnees
from Frontend.Siscrire import Apk
from dotenv import load_dotenv
import sqlite3
import os
import hashlib
from datetime import datetime
from Backend.models import EtudiantManager,CodeVerificationManager

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

        self.sexe = ["Homme", "Femme"]
        self.niv_scolaire  = ["6éme année primaire", "3ème année collége", "Niveau Bac", "Baccalauréat"]
        self.CreatInterface()
    
    def CreatInterface(self):
        self.pathReturn = Path("./Custom/pic/return.png").resolve()
        self.picReturn = CreateImage(str(self.pathReturn), width=20, height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_accueil,fg_color=self.theme_data["title"])
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
        self.nom.EntryPlace(0.27, 0.29, "center")

        self.prenom = CreatEntry(self, 235, 42, 7, 0, placeholder_text="Votre Prenom *",Font_size=12)
        self.prenom.EntryPlace(0.73, 0.29, "center")

        self.Sexe=CreatComboBox(self,self.sexe,235,42,fg_color="white",bg_color="transparent",text_color="#9E9E9E",corner_radius=7, state="readonly",button_color=self.theme_data["button_hover"],border_width=0)
        self.Sexe.ComboBoxPlace(0.27, 0.39, "center")
        self.Sexe.set("Votre Sexe *")

        self.dateNaissance=CreatEntry(self,235,42,7,0,placeholder_text="Votre Date Naissance *",Font_size=12)
        self.dateNaissance.EntryPlace(0.73,0.39,"center")

        self.Bac=CreatEntry(self,235,42,7,0,placeholder_text="Votre Année de bac *",Font_size=12)
        self.Bac.EntryPlace(0.27,0.49,"center")

        self.Niv_Scolaire=CreatComboBox(self,self.niv_scolaire,235,42,fg_color="white",bg_color="transparent",text_color="#9E9E9E",corner_radius=7, state="readonly",button_color=self.theme_data["button_hover"],border_width=0)
        self.Niv_Scolaire.ComboBoxPlace(0.73,0.49,"center")
        self.Niv_Scolaire.set("Votre Niveau scolaire *")

        self.Filiere=CreatComboBox(self,[],485,42,fg_color="white",bg_color="transparent",text_color="#9E9E9E",corner_radius=7, state="readonly",button_color=self.theme_data["button_hover"],border_width=0)
        self.Filiere.ComboBoxPlace(0.5,0.59,"center")
        self.Filiere.set("Votre Filiéres *")

        self.Niv_Scolaire.ComboBoxConfig(command=lambda value: self.check_niveau())

        self.email=CreatEntry(self,485,42,7,0,placeholder_text="Votre Email *",Font_size=12)
        self.email.EntryPlace(0.5,0.69,"center")

        self.buttonConnect=CreatButton(self,"Valide",485,35,command=self.valide_formulaire,fg_color=self.theme_data["title"])
        self.buttonConnect.buttonPlace(0.5,0.80,"center")
        self.buttonConnect.buttonConfig(font=(self.type_font,14,"bold"))

        self.ConnecteAccount=CreatButton(self,"Vous avez un compte ? Connectez-vous ici",text_color="#B0B0B0",hover_color="#2C3440",fg_color="transparent",corner_radius=7,height=30,command=self.change_to_connecte)
        self.ConnecteAccount.buttonPlace(0.5,0.87,"center")
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

        self.footer.LabelPlace(relx=0.5,rely=0.94,anchor="center")
        self.show_Frame()

    def check_niveau(self):
        selected_niveau = self.Niv_Scolaire.get()

        if selected_niveau == "6éme année primaire":
            self.filières_ofppt = [
                "Gestion Hôtelière", "Génie Civil", "Électromécanique", "Mécanique",
                "Électricité", "Gestion", "Tourisme", "BTP (Bâtiment et Travaux Publics)"
            ]
        elif selected_niveau == "Baccalauréat":
            self.filières_ofppt = [
                "Développement Digital", "Réseaux Informatiques", "Gestion des Entreprises",
                "Gestion Hôtelière", "Génie Civil", "Électromécanique", "Gestion",
                "Tourisme", "BTP (Bâtiment et Travaux Publics)"
            ]
        elif selected_niveau == "Niveau Bac":
            self.filières_ofppt = [
                "Développement Digital", "Réseaux Informatiques", "Génie Civil",
                "Pâtisserie", "Métiers de la Coiffure et Esthétique", 
                "Plomberie Sanitaire", "Menuiserie Aluminium et Bois"
            ]
        elif selected_niveau == "3ème année collége":
            self.filières_ofppt = [
                "Pâtisserie", "Métiers de la Coiffure et Esthétique", 
                "Plomberie Sanitaire", "Menuiserie Aluminium et Bois"
            ]
        else:
            self.filières_ofppt=[]
        
        self.Filiere.ComboBoxConfig(values=self.filières_ofppt)
        self.Filiere.set("Votre Filiéres *")



    def on_entre(self,event):
        self.ConnecteAccount.buttonConfig(text_color=self.theme_data["text"])
   
    def on_leave(self,event):
        self.ConnecteAccount.buttonConfig(text_color="#B0B0B0")
    
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
    
    def change_to_connecte(self):
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

    def validate_nom_prenom(self, valeur, champ_nom):
        if not valeur:
            messagebox.showerror("Erreur", f"Le {champ_nom} est obligatoire.")
            return False
        if len(valeur) < 2:
            messagebox.showerror("Erreur", f"Le {champ_nom} doit contenir au moins 2 caractères.")
            return False
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$', valeur):
            messagebox.showerror("Erreur", f"Le {champ_nom} contient des caractères invalides.")
            return False
        return True



    def validate_sexe(self, sexe):
        if not sexe:
            messagebox.showerror('error', 'Le sexe est obligatoire.')
            return False
        sexe = sexe.lower()
        if sexe not in ['homme', 'femme']:
            messagebox.showerror('error', "Veuillez entrer 'Homme', 'Femme'")
            return False
        return True
    
    def validate_date_naissance(self, date_str):
        if not date_str:
            messagebox.showerror('error','La date de naissance est obligatoire.')
            return False
        date_formats=["%d/%m/%Y","%d-%m-%Y"]
        for i in date_formats:
            try:
                date_obj = datetime.strptime(date_str, i)
                now = datetime.now()

                if date_obj > now:
                    messagebox.showerror('error', 'La date de naissance doit être dans le passé.')
                    return False

                age = now.year-date_obj.year-((now.month, now.day) < (date_obj.month, date_obj.day))
                if age < 15:
                    messagebox.showerror('error', 'Vous devez avoir au moins 15 ans pour vous inscrire.')
                    return False
                
                return True
            except ValueError:
                pass
        messagebox.showerror('error','Format de date invalide. Utilisez JJ/MM/AAAA ou JJ-MM-AAAA.')
        return False


    def validate_bac_year(self, year_str):
        if not year_str:
            messagebox.showerror('error', 'L\'année du bac est obligatoire.')
            return False

        try:
            year = int(year_str)
            if 2013 <= year <= 2025:
                return True
            else:
                messagebox.showerror('error', 'L\'année du bac doit être entre 2013 et 2025.')
                return False
        except ValueError:
            messagebox.showerror('error', 'Format invalide. Entrez une année valide (ex: 2018).')
            return False


    def validate_dropdowns(self):
        if self.Niv_Scolaire.get()=="Votre Niveau scolaire *":
            messagebox.showerror("error", "Veuillez sélectionner un niveau scolaire.")
            return False
        if self.Bac.get() == "Votre Année de bac *":
            messagebox.showerror("error", "Veuillez sélectionner un type de Bac.")
            return False
        if self.Filiere.get() == "Votre Filiéres *":
            messagebox.showerror("error", "Veuillez sélectionner un type de Filiére.")
            return False
        return True
    
    def validate_email(self, email):
        if not email:
            messagebox.showerror('error', "L'adresse email est obligatoire.")
            return False
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            messagebox.showerror('error', "Format d'email invalide.")
            return False

        common_domains={
            'gmail.co':'gmail.com',
            'gmail.fr':'gmail.com',
            'gmial.com':'gmail.com',
            'gamil.com':'gmail.com',
            'yahooo.com':'yahoo.com',
            'yaho.com':'yahoo.com',
            'hotmial.com':'hotmail.com',
            'hotmil.com':'hotmail.com',
            'outook.com':'outlook.com'
        }
        domain = email.split('@')[-1]
        if domain in common_domains:
            corrected_domain = common_domains[domain]
            corrected_email = email.replace(domain, corrected_domain)
            messagebox.showerror('error', f"Vouliez-vous dire {corrected_email}?")
            return False
        return True
    
    def valide_formulaire(self):
        try:
            nom = self.nom.get().strip()
            prenom = self.prenom.get().strip()
            email = self.email.get().strip()
            sexe = self.Sexe.get().strip()
            dateNaissance = self.dateNaissance.get().strip()

            valide_nom = self.validate_nom_prenom(nom, "nom")
            valide_prenom = self.validate_nom_prenom(prenom, "prénom")
            valide_email = self.validate_email(email)
            valide_date = self.validate_date_naissance(dateNaissance)
            valide_sexe = self.validate_sexe(sexe)
            valide_bac = self.validate_bac_year(self.Bac.get().strip())
            valide_dropdown = self.validate_dropdowns()

            all_valide = [valide_email, valide_nom, valide_prenom, valide_sexe, valide_date, valide_dropdown, valide_bac]

            if all(all_valide):
                if self.EtudiantManager.email_existe(email):
                    messagebox.showwarning("Adresse e-mail déjà utilisée",
                        "Cette adresse e-mail est déjà utilisée par un autre compte. Veuillez saisir une autre adresse e-mail, s’il vous plaît.")
                    return
                else:
                    messagebox.showinfo("Succès", "Inscription enregistrée. Veuillez vérifier votre email.")
                    self.sendEmailCode(email)
                    self.change_to_otp(email)
        except Exception as e:
            print(f"Erreur: {e}")  # pour debug si besoin
            messagebox.showerror("Erreur système", f"Une erreur inattendue s'est produite: {str(e)}")

    
    def change_to_otp(self,email):
        from Frontend.OTP_Email import OTP_Email
        self.destroy()
        manager = ChangeFrame(self.master)
        manager.show_frame(lambda parent: OTP_Email(parent, "test.csv", "proof",email))

    def sendEmailCode(self, Email_receiver):
        load_dotenv()
        email_sender = str(os.getenv("EMAIL_SENDER"))
        email_password = str(os.getenv("EMAIL_PASSWORD"))
        email_receiver = Email_receiver

        Subject = "Votre Code de Vérification - DD-NOTE-OFPPT"
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
                <title>Réinitialisation de mot de passe</title>
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
                                                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">Réinitialisation de mot de passe</h1>
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
                                                    <p style="font-size: 16px; line-height: 24px; margin: 0 0 30px 0;">Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte DD-NOTE-OFPPT. Pour assurer la sécurité de votre compte, veuillez utiliser le code de vérification ci-dessous.</p>
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
                                                                    📧 support@ddnote-ofppt.ma<br>
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
                                                    <p style="margin: 0; color: white; font-size: 14px;">© 2025 DD-NOTE-OFPPT. Tous droits réservés.</p>
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