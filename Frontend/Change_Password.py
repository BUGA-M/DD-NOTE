import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel, CreatEntry, CreatButton, CreatFrame, CreatComboBox, FontInstaller, ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
from Frontend.connexion import ConnexionFrame
import re,csv
from Backend.models import EtudiantManager,CodeVerificationManager,Validation
from datetime import datetime
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
import ssl
#from Backend.exceptions import InvalidPasswordException,StrongPasswordException

class CreatChangePassword(CreatFrame):
    def __init__(self, master, NameDateBase, type,Email):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(master, 450, 450, "transparent", self.theme_data["button"], 20)
        self.type=type
        self.datebase=NameDateBase
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.CreatInterfacePass()
        #self.basedonnee=BaseDonnees()
        self.EmailClient = Email
        self.EtudiantManager=EtudiantManager()
        self.Validation_class = Validation()

    def CreatInterfacePass(self):
        self.labeltitel = CreatLabel(self, "Changer Mot De Passe", 28, self.title_font[0])
        self.labeltitel.LabelPlace(0.5, 0.17, "center")
        self.labeltitel.LabelConfig(font=(self.title_font[0], 29, "bold"))

        self.ligne = CreatFrame(self, 385, 2, fg_color="#dfdddb")
        self.ligne.FramePlace(0.5, 0.26, "center")

        self.passNou_sub = CreatLabel(self, "Veuillez entrer votre nouveau mot de passe.", 12, self.subtitle_font, self.theme_data["text"], "transparent")
        self.passNou_sub.LabelPlace(0.5, 0.32, "center")

        self.NouvPassword = CreatEntry(self, 350, 44)
        self.NouvPassword.EntryConfig(placeholder_text="Nouveau mot de passe", font=(self.type_font, 13), corner_radius=7, show="*")
        self.NouvPassword.EntryPlace(0.5, 0.45, "center")

        self.Confirmation_Password = CreatEntry(self, 350, 44, 7, 0)
        self.Confirmation_Password.EntryConfig(placeholder_text="Confirmation de mot de passe", font=(self.type_font, 13), corner_radius=7, show="*")
        self.Confirmation_Password.EntryPlace(0.5, 0.62, "center")

        self.buttonConnect = CreatButton(self, "Valide", 350, 35)
        self.buttonConnect.buttonPlace(0.5, 0.78, "center")
        self.buttonConnect.buttonConfig(font=(self.type_font, 14, "bold"), command=lambda : self.valide_password(),fg_color=self.theme_data["title"])

        self.footer = CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="white",
            bg_color="transparent"
        )
        self.footer.LabelPlace(relx=0.5, rely=0.95, anchor="center")
        self.show_Frame()
    
    def valide_password(self):
        password = self.NouvPassword.get().strip()
        conf_password = self.Confirmation_Password.get().strip()
        Password_Valider = self.Validation_class.validate_password(password, conf_password)
        
        if Password_Valider and self.EtudiantManager.changer_password(self.EmailClient,Password_Valider) :
            messagebox.showinfo('Succès', 'Le mot de passe a été modifié avec succès.')
            self.NouvPassword.delete(0, 'end')
            self.Confirmation_Password.delete(0, 'end')
            self.sendEmail(self.EmailClient)
            self._perform_Go_to_connecte()
            #self.returnAccueil()
        else :
            messagebox.showerror(
            "Erreur de mot de passe",
            "❌ Le mot de passe que vous avez saisi est identique à l'ancien.\n\n"
            "🔒Veuillez choisir un mot de passe différent pour des raisons de sécurité."
        )

    
    
    def show_Frame(self):
        self.FramePlace(relx=0.5, rely=0.5, anchor="center")
        
    def _perform_Go_to_connecte(self):
        from Frontend.Siscrire import Apk
        self.destroy()
        manager=ChangeFrame(self.master)
        if self.type == "admin" :
            manager.show_frame(lambda parent:Apk(parent,"Enter your code","Enter your password","admin.csv","admin"))
        if self.type == "Stagaire" :
            manager.show_frame(lambda parent: Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"))
        if self.type == "Formateur" :
            manager.show_frame(lambda parent:Apk(parent,"Enter your CIN","Enter your password","Formateur.csv","Formateur"))
    
    
    def returnAccueil(self):
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

    def sendEmail(self, Email_receiver):
        load_dotenv()
        email_sender = str(os.getenv("EMAIL_SENDER"))
        email_password = str(os.getenv("EMAIL_PASSWORD"))
        email_receiver = Email_receiver

        Subject = "Notification de Changement de Mot de Passe"
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = Subject
        context = ssl.create_default_context()

        now = datetime.now()
        date_changement = now.strftime("%d/%m/%Y")
        heure_changement = now.strftime("%H:%M")

        # Corps de l'email version HTML avec style pro
        html_content = f"""\
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Notification de Changement de Mot de Passe</title>
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
                                    <td style="background: linear-gradient(135deg, {self.theme_data['title']}, {self.theme_data['footer']}); padding: 30px 0; text-align: center; border-radius: 10px 10px 0 0;">
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
                                                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">Notification de Changement de Mot de Passe</h1>
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
                                                    <p style="font-size: 18px; font-weight: 500; margin: 0 0 20px 0; color: {self.theme_data['title']}">Bonjour</p>
                                                    <p style="font-size: 16px; line-height: 24px; margin: 0 0 20px 0;">
                                                        Nous vous informons que le mot de passe de votre compte DD-NOTE a été modifié avec succès le <span style="font-weight: 600;">{date_changement}</span> à <span style="font-weight: 600;">{heure_changement}</span>.
                                                    </p>
                                                    <p style="font-size: 16px; line-height: 24px; margin: 0 0 30px 0;color: #374151;">
                                                        Si vous êtes à l'origine de cette modification, aucune action n'est requise de votre part.
                                                    </p>
                                                </td>
                                            </tr>
                                            
                                            <!-- Warning -->
                                            <tr>
                                                <td style="padding: 20px 0;">
                                                    <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #fef2f2; border-radius: 6px; border-left: 4px solid #fbbf24;">
                                                        <tr>
                                                            <td style="padding: 15px; display: flex;">
                                                                <table role="presentation" style="border-collapse: collapse; border:0; border-spacing:0;">
                                                                    <tr>
                                                                        <td width="30" style="vertical-align: top; padding-right: 15px;">
                                                                            <!-- Alert Icon -->
                                                                            <div style="width: 24px; height: 24px; font-weight: bold; color: #d97706; text-align: center;">⚠️</div>
                                                                        </td>
                                                                        <td>
                                                                            <div style="font-weight: 500; color: #92400e; font-size: 15px; line-height: 22px;">
                                                                                Si vous n'avez pas effectué ce changement de mot de passe, veuillez immédiatement contactez notre équipe de support ou le responsable de votre filière pour sécuriser votre compte .
                                                                            </div>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                            
                                            <!-- Security tips -->
                                            <tr>
                                                <td style="padding: 20px 0;">
                                                    <table role="presentation" style="width:100%; border-collapse: collapse; border:0; border-spacing:0; background-color: #f3f4f6; border-radius: 10px;">
                                                        <tr>
                                                            <td style="padding: 25px;">
                                                                <h3 style="margin-top: 0; color: {self.theme_data['title']}; font-size: 18px; font-weight: 600; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid {self.theme_data['title']}; display: inline-block;">Conseils de sécurité</h3>
                                                                <ul style="margin: 0; padding-left: 20px;">
                                                                    <li style="font-size: 15px; line-height: 24px; margin-bottom: 8px;">Utilisez un mot de passe unique pour chaque service en ligne</li>
                                                                    <li style="font-size: 15px; line-height: 24px; margin-bottom: 8px;">Contactez le responsable de votre filière </li>
                                                                    <li style="font-size: 15px; line-height: 24px;">Vérifiez régulièrement l'activité de votre compte</li>
                                                                </ul>
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
                                                    <div style="height: 1px; background-color: rgba(255, 255, 255, 0.2); width: 80%;"></div>
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
        Changement de mot de passe - DD-NOTE

        Bonjour,

        Nous vous informons que le mot de passe associé à votre compte sur DD-NOTE a été modifié avec succès.

        Si vous êtes à l'origine de cette modification, aucune action supplémentaire n'est requise.
        Dans le cas contraire, nous vous recommandons de sécuriser immédiatement votre compte en contactant notre support.

        Merci de votre confiance.

        Cordialement,
        L'équipe DD-NOTE
        """

        # Ajouter les deux versions au message
        em.set_content(text_content)
        em.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.send_message(em)
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {str(e)}")