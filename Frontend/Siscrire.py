import customtkinter as ctk
from tkinter import messagebox
import csv
from Frontend.ForgetPassword import ForgetPassword
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
from pathlib import Path
from Backend.models import EtudiantManager

class Apk(CreatFrame):
    def __init__(self,master,Entrykey,password,NameDateBase,type):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(
            master,
            450,
            500,
            "transparent",
            self.theme_data["button"], 
            20   
        )
        self.entry_key=Entrykey
        self.psw=password
        self.NameDateBase=NameDateBase
        self.type=type
        self.EtudiantManager=EtudiantManager()
        self.CreatConnecter()
    def CreatConnecter(self):
        title_font=FontInstaller.get_font("Titan One")
        subtitle_font=FontInstaller.get_font("Poppins")
        type_font=FontInstaller.get_font("Orbitron")

        self.pathReturn=Path("./Custom/pic/return.png").resolve()
        self.picReturn=CreateImage(str(self.pathReturn),width=20,height=20)
        
        self.pathHide=Path("./Custom/pic/eye_hide.png").resolve()
        self.picHide=CreateImage(str(self.pathHide),width=20,height=20)
        
        self.pathWatch=Path("./Custom/pic/eye_watch.png").resolve()
        self.picWatch=CreateImage(str(self.pathWatch),width=20,height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_accueil,fg_color=self.theme_data["title"])
        self.returnButton.buttonPlace(0.09,0.08,"center")
        self.returnButton.buttonConfig(font=(type_font,14,"bold"))
        

        self.LabelConnect=CreatLabel(self,"Ce connecter",30,title_font)
        #self.LabelConnect.LabelConfig(bg_color="#343A40")
        self.LabelConnect.LabelPlace(0.5,0.15,"center")

        self.ligne=CreatFrame(self,385,2,fg_color="#dfdddb")
        self.ligne.FramePlace(0.5,0.22,"center")

        self.subtitle=CreatLabel(self,"Bienvenue! Veuillez saisir vos coordonnées",13,subtitle_font,"#B0B0B0","transparent")
        self.subtitle.LabelPlace(0.5,0.27,"center")

        self.Entrykey=CreatEntry(self,350,44)
        self.Entrykey.EntryConfig(placeholder_text=self.entry_key,font=(type_font, 13),corner_radius=7)
        self.Entrykey.EntryPlace(0.5,0.42,"center")

        self.password=CreatEntry(self,350,44)
        self.password.EntryConfig(placeholder_text=self.psw,font=(type_font, 13),corner_radius=7,show="*")
        self.password.EntryPlace(0.5,0.57,"center")

        self.buttonConnect=CreatButton(self,"Connecter",350,35)
        self.buttonConnect.buttonPlace(0.5,0.72,"center")
        self.buttonConnect.buttonConfig(font=(type_font,14,"bold"),fg_color=self.theme_data["title"])
        if self.type.lower() == "stagaire":
            self.ConnecteAccount = CreatButton(
                self,
                "Vous n'avez pas de compte ? Inscrivez-vous ici",
                text_color="#B0B0B0",
                hover_color="#2C3440",
                fg_color="transparent",
                corner_radius=7,
                height=30,
                command=self.change_to_Inscrire
            )
            self.ConnecteAccount.buttonPlace(0.5, 0.81, "center")

            self.ConnecteAccount.bind("<Enter>", self.on_entre)
            self.ConnecteAccount.bind("<Leave>", self.on_leave)

        self.Watch_hide_Button = CreatButton(self, "", 40, 40, image=self.picHide.as_ctk(),corner_radius=7,command=self.toggle_password,fg_color=self.theme_data["title"],bg_color="white")
        self.Watch_hide_Button.buttonPlace(0.84,0.57,"center")
        self.Watch_hide_Button.buttonConfig(font=(type_font,14,"bold"))

        #self.ConnecteAccount=CreatButton(self,"Vous n'avez pas de compte ? Inscrivez-vous ici",text_color="#B0B0B0",hover_color="#2C3440",fg_color="transparent",corner_radius=7,height=30,command=self.change_to_Inscrire)
        #self.ConnecteAccount.buttonPlace(0.5,0.81,"center")

        #self.ConnecteAccount.bind("<Enter>", self.on_entre)
        #self.ConnecteAccount.bind("<Leave>", self.on_leave)

        self.ForgetPwConnect=CreatButton(self,"Mot de Passe oublier ?",160,26,lambda : self.change_to_ForgetMDP(),6,"transparent",text_color="#B0B0B0",hover_color="#2C3440")
        self.ForgetPwConnect.buttonPlace(0.5,0.87,"center")
        #self.ForgetPwConnect.buttonConfig(bg_color="transparent",font=(type_font,12,"bold"),text_color="#B0B0B0")
        
        self.ForgetPwConnect.bind("<Enter>", self.on_forget_enter)
        self.ForgetPwConnect.bind("<Leave>", self.on_forget_leave)

        
        self.footer=CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=11,
            text_font=subtitle_font[0],
            text_color="white",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.96,anchor="center")
        self.show_Frame()
        self.buttonConnect.configure(command=lambda: self.CheckConnect(self.type))
        
    def toggle_password(self):
        if self.password.cget("show") == "*":
            self.password.configure(show="") 
            self.Watch_hide_Button.configure(image=self.picWatch)
        else:
            self.password.configure(show="*") 
            self.Watch_hide_Button.configure(image=self.picHide)  
    def CheckConnect(self, Type, **kwargs):
        User = self.Entrykey.get().strip()
        password = self.password.get().strip()

        if not User or not password:
            match Type.lower():
                case "admin":
                    return messagebox.showerror("Erreur", "🛑 Identifiant et mot de passe requis pour l'administrateur.")
                case "formateur":
                    return messagebox.showerror("Erreur", "🛑 CIN et mot de passe requis pour le formateur.")
                case "stagaire":
                    return messagebox.showerror("Erreur", "🛑 Identifiant et mot de passe requis pour le stagiaire.")
                case _:
                    return messagebox.showerror("Erreur", "🛑 Type d'utilisateur inconnu.")

        Type_con = Type.lower()
        
        if Type_con == "stagaire":
            info = self.EtudiantManager.get_email_password_etudiant(User)
            if info and info["email"] == User and info["password"] == password:
                self.Entrykey.delete(0, "end")
                self.password.delete(0, "end")
                messagebox.showinfo("Succès", "✅ Connexion stagiaire réussie !")
                print("frame changer")
                self.Go_to_mainFrame(info["email"])
                return
            else:
                return messagebox.showerror("Erreur", "❌ Identifiant ou mot de passe stagiaire incorrect.")

        elif Type_con == "admin":
            print('base de donner pas encore cree')
            #info = self.AdminManager.get_admin_by_CODE(Code) 
            #if info and info["Code"] == User and info["password"] == password:
                #return messagebox.showinfo("Succès", "✅ Connexion administrateur réussie !")
            #else:
                #return messagebox.showerror("Erreur", "❌ Identifiant ou mot de passe administrateur incorrect.")

        elif Type_con == "formateur":
            print('base de donner pas encore cree')
            #info = self.ProfManager.get_prof_by_cin(User)  
            #if info and info["cin"] == User and info["password"] == password:
                #return messagebox.showinfo("Succès", "✅ Connexion formateur réussie !")
            #else:
                #return messagebox.showerror("Erreur", "❌ CIN ou mot de passe formateur incorrect.")
        else:
            return messagebox.showerror("Erreur", "❌ Type d'utilisateur non reconnu.")

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
    
    def Go_to_mainFrame(self,keyClient):
        from Frontend.mainFrame import CreateInterfaceGenerale
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: CreateInterfaceGenerale(parent,self.type,keyClient))
        
    def change_to_Inscrire(self):
        from Frontend.CreatAccount import CreatAccount
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent: CreatAccount(parent))

    def change_to_ForgetMDP(self):
        self.destroy()
        manager = ChangeFrame(self.master)
        manager.show_frame(lambda parent: ForgetPassword(parent, "test.csv", self.type))
        
    def on_entre(self, event):
        if hasattr(self, 'ConnecteAccount'):
            self.ConnecteAccount.buttonConfig(text_color=self.theme_data["text"])

    def on_leave(self, event):
        if hasattr(self, 'ConnecteAccount'):
            self.ConnecteAccount.buttonConfig(text_color="#B0B0B0")
        
    def on_forget_enter(self, event):
        self.ForgetPwConnect.buttonConfig(text_color=self.theme_data["text"])

    def on_forget_leave(self, event):
        self.ForgetPwConnect.buttonConfig(text_color="#B0B0B0")
        
    def show_Frame(self):
        self.FramePlace(relx=0.5,rely=0.5,anchor="center")


