import customtkinter as ctk
from tkinter import messagebox
import csv
from Frontend.ForgetPassword import ForgetPassword
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage
from pathlib import Path

class Apk(CreatFrame):
    def __init__(self,master,Entrykey,password,NameDateBase,type):
        super().__init__(
            master,
            450,
            450,
            "transparent",
            "#343A40", 
            20   
        )
        self.entry_key=Entrykey
        self.psw=password
        self.NameDateBase=NameDateBase
        self.type=type
        self.CreatConnecter()
    def CreatConnecter(self):
        title_font=FontInstaller.get_font("Titan One")
        subtitle_font=FontInstaller.get_font("Poppins")
        type_font=FontInstaller.get_font("Orbitron")

        self.pathReturn=Path("./Custom/pic/return.png").resolve()
        self.picReturn=CreateImage(str(self.pathReturn),width=20,height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_accueil,fg_color="transparent",hover_color="blue")
        self.returnButton.buttonPlace(0.1,0.1,"center")
        self.returnButton.buttonConfig(font=(type_font,14,"bold"))

        self.LabelConnect=CreatLabel(self,"Ce connecter",30,title_font,"#3b82f6")
        self.LabelConnect.LabelConfig(bg_color="#343A40")
        self.LabelConnect.LabelPlace(0.5,0.15,"center")

        self.ligne=CreatFrame(self,385,2,fg_color="#475569")
        self.ligne.FramePlace(0.5,0.22,"center")

        self.subtitle=CreatLabel(self,"Bienvenue! Veuillez saisir vos coordonnées",13,subtitle_font,"#B0B0B0","#343A40")
        self.subtitle.LabelPlace(0.5,0.27,"center")

        self.Entrykey=CreatEntry(self,350,44)
        self.Entrykey.EntryConfig(placeholder_text=self.entry_key,font=(type_font, 13),corner_radius=7)
        self.Entrykey.EntryPlace(0.5,0.42,"center")

        self.password=CreatEntry(self,350,44)
        self.password.EntryConfig(placeholder_text=self.psw,font=(type_font, 13),corner_radius=7)
        self.password.EntryPlace(0.5,0.57,"center")

        self.buttonConnect=CreatButton(self,"Connecter",350,35)
        self.buttonConnect.buttonPlace(0.5,0.72,"center")
        self.buttonConnect.buttonConfig(font=(type_font,14,"bold"))

        self.ConnecteAccount=CreatButton(self,"Vous n'avez pas de compte ? Inscrivez-vous ici",text_color="#B0B0B0",hover_color="#2C3440",fg_color="transparent",corner_radius=7,height=30,command=self.change_to_Inscrire)
        self.ConnecteAccount.buttonPlace(0.5,0.81,"center")

        self.ConnecteAccount.bind("<Enter>", self.on_entre)
        self.ConnecteAccount.bind("<Leave>", self.on_leave)

        self.ForgetPwConnect=CreatButton(self,"Forget Password ?",160,26,lambda : self.change_to_otp(),6,"transparent","#2C3440")
        self.ForgetPwConnect.buttonPlace(0.5,0.87,"center")
        self.ForgetPwConnect.buttonConfig(bg_color="#343A40",font=(type_font,12,"bold"),text_color="#AAAAAA")
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=subtitle_font[0],
            text_color="#64748b",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.93,anchor="center")
        self.show_Frame()
        self.buttonConnect.configure(command=lambda: self.CheckConnect(self.NameDateBase,self.type))
    def CheckConnect(self,NameDateBase,type,**kwarge):
        key=self.Entrykey.get().strip()
        password=self.password.get().strip()
        if key=="" or password=="":
            match type:
                case "admin":
                    return messagebox.showerror("Erreur","Both Id or password are required!")
                case "formateur":
                    return messagebox.showerror("Erreur","Both CIN or password are required!")
                case "stagaire":
                    return messagebox.showerror("Erreur","Both Id or password are required!")

        if(NameDateBase):
            with open(NameDateBase,'r',newline='',encoding='utf-8') as ficher:
                count=csv.reader(ficher,delimiter=';')
                for i in count:
                    if i[0]==key and i[1]==password:
                        messagebox.showinfo("Success", "Successful connection!")
                    elif i[0]!=key or i[0]!=password:
                        match type:
                            case "admin":
                                return messagebox.showerror("Erreur","Incorrect id or password")
                            case "formateur":
                                return messagebox.showerror("Erreur","Incorrect CIN or password")
                            case "stagaire":
                                return messagebox.showerror("Erreur","Incorrect id or password")
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
    
    def change_to_Inscrire(self):
        from Frontend.CreatAccount import CreatAccount
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: CreatAccount(parent))

    def change_to_otp(self):
        self.destroy()
        manager = ChangeFrame(self.master)
        manager.show_frame(lambda parent: ForgetPassword(parent, "test.csv", self.type))
    def on_entre(self,event):
        self.ConnecteAccount.buttonConfig(text_color="#3b82f6")
   
    def on_leave(self,event):
        self.ConnecteAccount.buttonConfig(text_color="#B0B0B0")
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")


