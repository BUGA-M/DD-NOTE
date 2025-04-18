import customtkinter as ctk
from tkinter import messagebox
import csv
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame

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

        self.LabelConnect=CreatLabel(self,"Ce connecter",30,title_font)
        self.LabelConnect.LabelConfig(bg_color="#343A40")
        self.LabelConnect.LabelPlace(0.5,0.17,"center")

        self.subtitle=CreatLabel(self,"Welcome back! Please enter your details",13,subtitle_font,"#B0B0B0","#343A40")
        self.subtitle.LabelPlace(0.5,0.26,"center")

        self.Entrykey=CreatEntry(self,350,44)
        self.Entrykey.EntryConfig(placeholder_text=self.entry_key,font=(type_font, 13),corner_radius=7)
        self.Entrykey.EntryPlace(0.5,0.42,"center")

        self.password=CreatEntry(self,350,44)
        self.password.EntryConfig(placeholder_text=self.psw,font=(type_font, 13),corner_radius=7)
        self.password.EntryPlace(0.5,0.60,"center")

        self.buttonConnect=CreatButton(self,"Connecter",350,35)
        self.buttonConnect.buttonPlace(0.5,0.76,"center")
        self.buttonConnect.buttonConfig(font=(type_font,14,"bold"))

        self.ForgetPwConnect=CreatButton(self,"Forget Password ?",160,26,"#",6,"transparent","#2C3440")
        self.ForgetPwConnect.buttonPlace(0.5,0.86,"center")
        self.ForgetPwConnect.buttonConfig(bg_color="#343A40",font=(type_font,13,"bold"),text_color="#AAAAAA")

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
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")


