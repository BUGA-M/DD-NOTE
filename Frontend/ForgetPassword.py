import smtplib
from email.message import EmailMessage
import ssl
import random
import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage
from Frontend.OTP import OTP
from Frontend.connexion import ConnexionFrame
import csv
from pathlib import Path


class ForgetPassword(CreatFrame):
    def __init__(self,master,NameDateBase,type):
        super().__init__(master,450,450,"transparent","#343A40",20)
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

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_connexion,fg_color="transparent",hover_color="blue")
        self.returnButton.buttonPlace(0.1,0.1,"center")
        self.returnButton.buttonConfig(font=(self.type_font,14,"bold"))

        self.labeltitel=CreatLabel(self,"Forget Password",28,self.title_font[0],"#3b82f6","transparent")
        self.labeltitel.LabelPlace(0.5,0.17,"center")
        self.labeltitel.LabelConfig(font=(self.title_font[0],29,"bold"))

        self.ligne=CreatFrame(self,385,2,fg_color="#475569")
        self.ligne.FramePlace(0.5,0.26,"center")

        self.SubEmail=CreatLabel(self,"Entrer Email Address",14,self.subtitle_font,"#B0B0B0","#343A40")
        self.SubEmail.LabelPlace(0.5,0.32,"center")


        self.EntryEmail=CreatEntry(self,350,44,7,0)
        self.EntryEmail.EntryConfig(placeholder_text="Exemple@email.com",font=(self.type_font, 13),corner_radius=7)
        self.EntryEmail.EntryPlace(0.5,0.46,"center")

        self.buttonConnect=CreatButton(self,"Send",350,35,lambda : self.checkEmail())
        self.buttonConnect.buttonPlace(0.5,0.63,"center")
        self.buttonConnect.buttonConfig(font=(self.type_font,14,"bold"))

        self.ligne_left=CreatFrame(self,80,2,fg_color="#475569")
        self.ligne_left.FramePlace(0.37,0.73,"center")
        
        self.LabelOu=CreatLabel(self,"OU",text_font=self.subtitle_font,text_color="#B0B0B0")
        self.LabelOu.LabelPlace(0.5,0.73,"center")

        self.ligne_right=CreatFrame(self,80,2,fg_color="#475569")
        self.ligne_right.FramePlace(0.63,0.73,"center")

        self.buttonAccountCreat=CreatButton(self,"Créer un compte",120,35,self.change_to_Inscrire,6,"transparent","#2C3440",text_color="#4299e1")
        self.buttonAccountCreat.buttonPlace(0.5,0.8,"center")
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="#64748b",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.90,anchor="center")
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
    
    def sendEmail(self,Email_receiver):
        email_sendaire='imadbenh255@gmail.com'
        email_password='gseldpmyibzsmpli'
        email_receiver=Email_receiver

        Subject="Votre Code de Vérification"
        em=EmailMessage()
        em['From']=email_sendaire
        em['To']=email_receiver
        em['Subject']=Subject
        
    
        context = ssl.create_default_context()
        code = str(random.randint(100000, 999999))
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                body = f"""
                Bonjour,

                Votre code de vérification est : {code}

                Ce code expirera dans 10 minutes.

                Merci,

                Votre Équipe d'Application DD-NOTE-OFPPT
                """
                em.set_content(body)
                smtp.login(email_sendaire, email_password)
                smtp.send_message(em)


            with open("FicherVerf.csv","w",newline='',encoding='utf-8') as ficher:
                writer=csv.writer(ficher,delimiter=";")
                writer.writerow([Email_receiver,code])

            messagebox.showinfo("Succès","Le code de vérification a été envoyé à votre adresse e-mail avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {e}")


    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
