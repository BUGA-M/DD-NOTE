import smtplib
from email.message import EmailMessage
import ssl
import random
import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
import csv
import time
import threading
import re
from Frontend.Change_Password import CreatChangePassword
from pathlib import Path

class OTP(CreatFrame):
    def __init__(self, master, NameDateBase, type):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(master, 450, 450, "transparent", self.theme_data["button"], 20)
        self.type = type
        self.datebase = NameDateBase
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.time_left = 300
        self.timer_running = False
        self.CreatInterfaceOTP()
    def CreatInterfaceOTP(self):
        #,self.title_font[0],"#3b82f6"
        self.pathReturn=Path("./Custom/pic/return.png").resolve()
        self.picReturn=CreateImage(str(self.pathReturn),width=20,height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=lambda : self.returnforget(),fg_color=self.theme_data["title"])
        self.returnButton.buttonPlace(0.09,0.08,"center")
        self.returnButton.buttonConfig(font=(self.type_font,14,"bold"))
        
        self.title_label=CreatLabel(self,"Vérifier le code",28,"transparent")
        self.title_label.LabelPlace(0.5,0.17,"center")
        self.title_label.LabelConfig(font=(self.title_font[0],29,"bold"))

        self.ligne=CreatFrame(self,385,2,fg_color="#dfdddb")
        self.ligne.FramePlace(0.5,0.26,"center")

        self.otp_sub=CreatLabel(self,"Veuillez saisir le code de vérification à 6 chiffres",12,self.subtitle_font,"#B0B0B0","transparent")
        self.otp_sub.LabelPlace(0.5,0.32,"center")


        self.timer_label = ctk.CTkLabel(
            self,
            text="Temps restant: 05:00",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.theme_data["text"]
        )
        self.timer_label.place(relx=0.5,rely=0.42,anchor="center")
        self.entry_frame=CreatFrame(self)
        self.entry_frame.FrameConfig(fg_color="transparent")
        self.entry_frame.FramePlace(0.5,0.54,"center")

        self.otp_entries=[]
        for i in range(6):
            entry=CreatEntry(
                self.entry_frame,
                40,
                45,
                8,
                2,
                justify="center",
                placeholder_text="",
                fg_color=self.theme_data["title"],
                border_color="black",
                text_color="white",
            )
            entry.EntryConfig(
                font=(self.type_font,18,"bold")
            )
            entry.grid(row=0,column=i,padx=5)
            entry.bind("<KeyRelease>", lambda e, index=i: self.move_to_next(e,index))
            self.otp_entries.append(entry)
        
        self.otp_entries[0].focus_set()

        self.resend_link =CreatButton(
            self,
            "Renvoyer le code",
            120,
            35,
            lambda : self.rensend_code(),
            6,
            "transparent",
            text_color=self.theme_data["text"],
        )
        self.resend_link.place(relx=0.5,rely=0.81,anchor="center")

        self.buttonVerif=CreatButton(self,"Vérifier",350,35,lambda : self.Verification_OTP())
        self.buttonVerif.buttonPlace(0.5,0.71,"center")
        self.buttonVerif.buttonConfig(font=(self.type_font,14,"bold"),fg_color=self.theme_data["title"])

        #self.buttonAccueil=CreatButton(self,"Revenir à l'écran d'accueil",120,35,lambda : self.returnAccueil(),6,"transparent","#2C3440",text_color="#4299e1")
        #self.buttonAccueil.buttonPlace(0.5,0.82,"center")
        
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="white",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.95,anchor="center")
        self.start_timer()
        self.show_Frame()
    
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
        
    def returnforget(self):
        from Frontend.ForgetPassword import ForgetPassword
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: ForgetPassword(parent, "test.csv", self.type))
    
    def sendEmail(self, Email_receiver):
        email_sender = 'imadbenh255@gmail.com'
        email_password = 'gseldpmyibzsmpli'
        email_receiver = Email_receiver

        Subject = "Votre Code de Vérification - DD-NOTE-OFPPT"
        em = EmailMessage()
        em['From'] = email_sender
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

            # Sauvegarder le code dans un fichier CSV
            with open("FicherVerf.csv", "w", newline='', encoding='utf-8') as ficher:
                writer = csv.writer(ficher, delimiter=";")
                writer.writerow([Email_receiver, code])

            messagebox.showinfo("Succès", "Le code de vérification a été envoyé à votre adresse e-mail avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {str(e)}") 
               
    def start_timer(self):
        if not self.timer_running:
            self.timer_running=True
            self.timer_thread=threading.Thread(target=self.update_timer)
            self.timer_thread.daemon=True
            self.timer_thread.start()
    
    def update_timer(self):
        while self.timer_running and self.time_left > 0:
            minutes,seconds=divmod(self.time_left, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            self.after(0,lambda t=time_str:self.timer_label.configure(text=f"Temps restant: {t}"))

            if self.time_left <= 120: 
                self.after(0,lambda:self.timer_label.configure(text_color="#3b82f6"))
                time.sleep(1)
                self.after(0,lambda:self.timer_label.configure(text_color="#e53e3e")) 
            time.sleep(1)
            self.time_left-=1
        if self.time_left==0:
            self.timer_running=False
            self.timer_label.configure(text="Temps expiré!")
            self.disable_verification()
   
    def disable_verification(self):
        for entry in self.otp_entries:
            entry.configure(state="disabled",border_width=0)
        self.label_expire=CreatLabel(
            self,
            "Le délai de validation est expiré. Veuillez demander un nouveau code.",
            12,
            self.subtitle_font)
        self.label_expire.LabelPlace(0.5,0.52,"center")
    
    
    def active_verfication(self):
        for entry in self.otp_entries:
            entry.configure(state="normal",border_width=2)
    
    def rensend_code(self):
        self.time_left=300
        self.timer_running=False
        self.start_timer()
        try:
            self.label_expire.LabelConfig(state="disabled")
        except:
            pass
        self.active_verfication()
        for entry in self.otp_entries:
            entry.delete(0, "end")
        self.otp_entries[0].focus_set()
        with open("FicherVerf.csv","r",newline='',encoding='utf-8') as ficher:
            count=csv.reader(ficher,delimiter=';')
            for i in count:
                Email=i[0]
        self.sendEmail(Email)
        try:
            self.label_expire.LabelConfig(state="disabled")
        except:
            pass
            
    def move_to_next(self,event,index):
        if not self.timer_running or self.time_left <= 0:
            return
            
        entry=self.otp_entries[index]
        value=entry.get()
        if value and not re.match(r"^\d$",value):
            entry.delete(0,"end")
            return
        if value and index< 5:
            self.otp_entries[index+1].focus_set()
        elif value and index == 5:
            self.Verification_OTP()
    
    def Verification_OTP(self):
        with open("FicherVerf.csv","r",newline='',encoding='utf-8') as ficher:
            count=csv.reader(ficher,delimiter=';')
            for i in count:
                Code=i[1]
        otp_code=''.join([entry.get() for entry in self.otp_entries])
        if len(otp_code)!=6:
            messagebox.showerror("error","Veuillez saisir 6 chiffres")
            for entry in self.otp_entries:
                entry.delete(0,"end")
            self.otp_entries[0].focus_set()
            return
        if not otp_code.isdigit():
            messagebox.showerror("error","Le code doit contenir uniquement des chiffres")
            for entry in self.otp_entries:
                entry.delete(0,"end")
            self.otp_entries[0].focus_set()
            return
        if otp_code==Code:
            self.timer_running=False
            messagebox.showinfo("Succès","Code OTP vérifié avec succès!")
            self.change_to_chnagePass()
        else:
            messagebox.showerror("error","Code OTP incorrect.")
            for entry in self.otp_entries:
                entry.delete(0, "end")
            self.otp_entries[0].focus_set()
            return
    def change_to_chnagePass(self):
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: CreatChangePassword(parent, "test.csv", "proof","imad"))
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
