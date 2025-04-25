import smtplib
from email.message import EmailMessage
import ssl
import random
import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
from Frontend.OTP import OTP
from Frontend.connexion import ConnexionFrame
import csv
from pathlib import Path


class ForgetPassword(CreatFrame):
    def __init__(self,master,NameDateBase,type):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(master,450,450,"transparent",self.theme_data["button"],20)
        self.type=type
        self.datebase=NameDateBase
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.time_left=300
        self.timer_running=False
        self.creatforget()
   
    def creatforget(self):
        self.pathReturn=Path("./Custom/pic/return.png").resolve()
        self.picReturn=CreateImage(str(self.pathReturn),width=20,height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_connexion,fg_color=self.theme_data["title"])
        self.returnButton.buttonPlace(0.09,0.08,"center")
        self.returnButton.buttonConfig(font=(self.type_font,14,"bold"))

        self.labeltitel=CreatLabel(self,"Recuperation Mot de Passe",28,self.title_font)
        self.labeltitel.LabelPlace(0.5,0.2,"center")
        self.labeltitel.LabelConfig(font=(self.title_font[0],25,"bold"))

        #self.ligne=CreatFrame(self,385,2,fg_color="#dfdddb")
        #self.ligne.FramePlace(0.5,0.26,"center")

        self.SubEmail=CreatLabel(self,"Entrer Votre Address Email ",14,self.subtitle_font,"#B0B0B0","transparent")
        self.SubEmail.LabelPlace(0.5,0.32,"center")


        self.EntryEmail=CreatEntry(self,350,44,7,0)
        self.EntryEmail.EntryConfig(placeholder_text="Exemple@email.com",font=(self.type_font, 13),corner_radius=7)
        self.EntryEmail.EntryPlace(0.5,0.46,"center")

        self.buttonConnect=CreatButton(self,"Send",350,35,lambda : self.checkEmail())
        self.buttonConnect.buttonPlace(0.5,0.63,"center")
        self.buttonConnect.buttonConfig(font=(self.type_font,14,"bold"),fg_color=self.theme_data["title"])

        if self.type.lower() == "stagaire":
            self.ligne_left=CreatFrame(self,160,2,fg_color="#dfdddb")
            self.ligne_left.FramePlace(0.27,0.73,"center")
            
            self.LabelOu=CreatLabel(self,"OU",text_font=self.subtitle_font,text_color="#dfdddb")
            self.LabelOu.LabelPlace(0.5,0.73,"center")

            self.ligne_right=CreatFrame(self,160,2,fg_color="#dfdddb")
            self.ligne_right.FramePlace(0.73,0.73,"center")
            
            self.buttonAccountCreat=CreatButton(self,"Créer un compte",120,35,self.change_to_Inscrire,6,"transparent","#2C3440",text_color="#B0B0B0")
            self.buttonAccountCreat.buttonPlace(0.5,0.8,"center")
               
            self.buttonAccountCreat.bind("<Enter>", self.on_forget_enter)
            self.buttonAccountCreat.bind("<Leave>", self.on_forget_leave)
        else:
            warning_text = "⚠️ Contactez l'administration\nsi vous avez perdu votre EMAIL"
            info_label = CreatLabel(
                self,
                warning_text,
                13,
                self.subtitle_font,
                text_color=self.theme_data["text"],
                bg_color="transparent",
                justify="center"
            )
            info_label.LabelPlace(0.5, 0.81, "center")


        
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="white",
            bg_color="transparent",
        )

        self.footer.LabelPlace(relx=0.5,rely=0.95,anchor="center")
        self.show_Frame()
    
    def change_to_Inscrire(self):
        from Frontend.CreatAccount import CreatAccount
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: CreatAccount(parent))
    
    def change_to_connexion(self):
        from Frontend import Apk
        self.destroy()
        manager=ChangeFrame(self.master)
        if self.type=="admin":
            manager.show_frame(lambda parent:Apk(parent,"Enter your code","Enter your password","admin.csv","admin"))
        elif self.type=="Stagaire":
            manager.show_frame(lambda parent:Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"))
        elif self.type=="Formateur":
            manager.show_frame(lambda parent:Apk(parent,"Enter your CIN","Enter your password","Formateur.csv","Formateur"))
    def change_to_otp(self):
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: OTP(parent, "test.csv", "proof"))

    def checkEmail(self):
        Email=self.EntryEmail.get().strip()
        if not Email:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse email")
            return
        if '@' not in Email:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse email valide")
            return
        found=False
        with open(self.datebase,"r",newline='',encoding="utf-8") as ficher:
            count=csv.reader(ficher,delimiter=";")
            for i in count:
                if i[0]==Email:
                    found=True
                    self.sendEmail(Email)
                    break
        if not found:
            messagebox.showerror("Erreur","Adresse e-mail non trouvée dans la base de données.")
            return
        self.after(10, self.change_to_otp) 
    
    def sendEmail(self, Email_receiver):
        import smtplib
        from email.message import EmailMessage
        import ssl
        import random
        import csv

        email_sendaire = 'imadbenh255@gmail.com'
        email_password = 'gseldpmyibzsmpli'
        email_receiver = Email_receiver

        Subject = "Votre Code de Vérification - DD-NOTE-OFPPT"
        em = EmailMessage()
        em['From'] = email_sendaire
        em['To'] = email_receiver
        em['Subject'] = Subject

        context = ssl.create_default_context()
        code = str(random.randint(100000, 999999))

        # Corps de l’email version HTML avec style pro
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


        # Contenu brut (obligatoire pour fallback)
        em.set_content("Votre code de vérification est : " + code)
        em.add_alternative(html_content, subtype="html")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sendaire, email_password)
                smtp.send_message(em)

            # Écriture du code dans un fichier CSV temporaire
            with open("FicherVerf.csv", "w", newline='', encoding='utf-8') as ficher:
                writer = csv.writer(ficher, delimiter=";")
                writer.writerow([Email_receiver, code])

            from tkinter import messagebox
            messagebox.showinfo("Succès", "Le code de vérification a été envoyé à votre adresse e-mail avec succès.")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {e}")

                
    def on_forget_enter(self, event):
        self.buttonAccountCreat.buttonConfig(text_color=self.theme_data["text"])

    def on_forget_leave(self, event):
        self.buttonAccountCreat.buttonConfig(text_color="#B0B0B0")

    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
