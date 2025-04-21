import smtplib
from email.message import EmailMessage
import ssl
import random
import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame
import csv
import time
import threading
import re
class OTP(CreatFrame):
    def __init__(self, master, NameDateBase, type):
        super().__init__(master, 450, 450, "transparent", "#343A40", 20)
        self.type = type
        self.datebase = NameDateBase
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.time_left = 300
        self.timer_running = False
        self.CreatInterfaceOTP()
    def CreatInterfaceOTP(self):
        self.title_label=CreatLabel(self,"Vérifier le code",28,self.title_font[0],"#3b82f6","transparent")
        self.title_label.LabelPlace(0.5,0.17,"center")
        self.title_label.LabelConfig(font=(self.title_font[0],29,"bold"))

        self.ligne=CreatFrame(self,385,2,fg_color="#475569")
        self.ligne.FramePlace(0.5,0.26,"center")

        self.otp_sub=CreatLabel(self,"Veuillez saisir le code de vérification à 6 chiffres",12,self.subtitle_font,"#B0B0B0","#343A40")
        self.otp_sub.LabelPlace(0.5,0.32,"center")


        self.timer_label = ctk.CTkLabel(
            self,
            text="Temps restant: 05:00",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color="#e53e3e"
        )
        self.timer_label.place(relx=0.5,rely=0.4,anchor="center")
        self.entry_frame=CreatFrame(self)
        self.entry_frame.FrameConfig(fg_color="transparent")
        self.entry_frame.FramePlace(0.5,0.52,"center")

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
                fg_color="#343A40",
                text_color="white"
            )
            entry.EntryConfig(
                font=(self.type_font,18,"bold")
            )
            entry.grid(row=0,column=i,padx=5)
            entry.bind("<KeyRelease>", lambda e, index=i: self.move_to_next(e, index))
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
            "#2C3440",
            text_color="#4299e1",
        )
        self.resend_link.place(relx=0.5,rely=0.65,anchor="center")

        self.buttonVerif=CreatButton(self,"Vérifier",350,35,lambda : self.Verification_OTP())
        self.buttonVerif.buttonPlace(0.5,0.77,"center")
        self.buttonVerif.buttonConfig(font=(self.type_font,14,"bold"))

        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=self.subtitle_font[0],
            text_color="#64748b",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.90,anchor="center")
        self.start_timer()
        self.show_Frame()
    
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
            self.destroy()
        else:
            messagebox.showerror("error","Code OTP incorrect.")
            for entry in self.otp_entries:
                entry.delete(0, "end")
            self.otp_entries[0].focus_set()
            return

    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")
