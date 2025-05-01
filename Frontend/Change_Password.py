import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel, CreatEntry, CreatButton, CreatFrame, CreatComboBox, FontInstaller, ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors,BaseDonnees
from Frontend.connexion import ConnexionFrame
import re,csv

class InvalidPasswordException(Exception):
    def __init__(self, message="Le mot de passe ne correspond pas."):
        super().__init__(message)
        messagebox.showerror('Erreur', message)

class StrongPasswordException(Exception):
    def __init__(self, message="Le mot de passe est faible. Il doit comporter plus de 8 caractères, dont des majuscules, des minuscules et des chiffres."):
        super().__init__(message)
        messagebox.showerror('Erreur', message)

def validate_password(password, confirm_password):
    if password != confirm_password:
        raise InvalidPasswordException()
    if len(password) <= 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        raise StrongPasswordException()
    return True

class CreatChangePassword(CreatFrame):
    def __init__(self, master, NameDateBase, type):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(master, 450, 450, "transparent", self.theme_data["button"], 20)
        self.type=type
        self.datebase=NameDateBase
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.CreatInterfacePass()
        self.basedonnee=BaseDonnees()

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
        try:
            password = self.NouvPassword.get().strip()
            conf_password = self.Confirmation_Password.get().strip()
            
            if not password or not conf_password:
                messagebox.showerror('Erreur', 'Veuillez remplir tous les champs.')
                return

            if validate_password(password, conf_password):
                if self.update_password(password):
                    messagebox.showinfo('Succès', 'Le mot de passe a été modifié avec succès.')
                    self.NouvPassword.delete(0, 'end')
                    self.Confirmation_Password.delete(0, 'end')
                    self.returnAccueil()
                    
        except (InvalidPasswordException, StrongPasswordException) as e:
            pass
        except Exception as e:
            messagebox.showerror('Erreur', f'Une erreur est survenue: {str(e)}')

    def update_password(self,new_password):
        try:
            with open("ForgetPss.csv","r",newline="",encoding="utf-8") as f:
                cur=csv.reader(f,delimiter=";")
                for i in cur:
                    Email=i[0]
            self.basedonnee.mettre_a_jour_mot_de_passe(Email,new_password)
            return True
            
        except Exception as e:
            messagebox.showerror('Erreur', f"Impossible de mettre à jour le mot de passe: {str(e)}")
            return False
    
    def show_Frame(self):
        self.FramePlace(relx=0.5, rely=0.5, anchor="center")
    
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

