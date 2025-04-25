import customtkinter as ctk
from tkinter import messagebox
import csv,re
from pathlib import Path
from datetime import datetime
from Frontend.ForgetPassword import ForgetPassword
from Custom import CreatLabel,CreatEntry,CreatButton,CreatFrame,CreatComboBox,FontInstaller,ChangeFrame,CreateImage
from Frontend.Siscrire import Apk
from Frontend.connexion import ConnexionFrame

class CreatAccount(CreatFrame):
    def __init__(self,master):
        super().__init__(
            master,
            550,
            550,
            "transparent",
            "#343A40", 
            20   
        )
        self.title_font=FontInstaller.get_font("Titan One")
        self.subtitle_font=FontInstaller.get_font("Poppins")
        self.type_font=FontInstaller.get_font("Orbitron")
        self.bac=["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
        self.niveau=["Tronc commun (sciences, lettres, etc.)","1ère année baccalauréat (sciences math, physique, SVT, économiques, techniques, etc.)","2ème année baccalauréat → Baccalauréat","Classe préparatoire (CPGE)","Brevet de Technicien Supérieur (BTS)","DUT / DEUG","Licence (professionnelle ou fondamentale)","Master","Doctorat"]
        self.CreatInterface()
    def CreatInterface(self):
        self.pathReturn=Path("./Custom/pic/return.png").resolve()
        self.picReturn=CreateImage(str(self.pathReturn),width=20,height=20)

        self.returnButton = CreatButton(self, "", 45, 45, image=self.picReturn.as_ctk(),corner_radius=7,command=self.change_to_sisncrire,fg_color="transparent",hover_color="blue")
        self.returnButton.buttonPlace(0.1,0.1,"center")
        self.returnButton.buttonConfig(font=(self.type_font,14,"bold"))



        self.LabelSinscrire=CreatLabel(self,"S'inscrire",30,self.title_font,"#3b82f6","transparent")
        self.LabelSinscrire.LabelPlace(0.5,0.09,"center")
        self.LabelSinscrire.LabelConfig(font=(self.title_font[0],29,"bold"))
        self.ligne=CreatFrame(self,385,2,fg_color="#475569")
        self.ligne.FramePlace(rely=0.14)

        self.subtitle=CreatLabel(self,"Bienvenue! Remplissez les champs selon présents dans votre identifiant",13,self.subtitle_font,"#B0B0B0","#343A40")
        self.subtitle.LabelPlace(0.5,0.19,"center")
        self.subtitle.LabelConfig(font=(self.subtitle,13,"bold"))

        self.nom=CreatEntry(self,235,42,7,0,placeholder_text="Votre Nom *",Font_size=12)
        self.nom.EntryPlace(0.27,0.29,"center")

        self.prenom=CreatEntry(self,235,42,7,0,placeholder_text="Votre Prenom *",Font_size=12)
        self.prenom.EntryPlace(0.73,0.29,"center")


        self.sexe=CreatEntry(self,235,42,7,0,placeholder_text="Votre Sexe *",Font_size=12)
        self.sexe.EntryPlace(0.27,0.39,"center")

        self.dateNaissance=CreatEntry(self,235,42,7,0,placeholder_text="Votre Date Naissance *",Font_size=12)
        self.dateNaissance.EntryPlace(0.73,0.39,"center")


        self.Bac=CreatComboBox(self,self.bac,235,42,fg_color="white",bg_color="transparent",text_color="#9E9E9E",corner_radius=7)
        self.Bac.ComboBoxPlace(0.27,0.49,"center")
        self.Bac.set("Votre Année de bac *")

        self.Niveau=CreatComboBox(self,self.niveau,235,42,fg_color="white",bg_color="transparent",text_color="#9E9E9E",corner_radius=7)
        self.Niveau.ComboBoxPlace(0.73,0.49,"center")
        self.Niveau.set("Votre Niveau scolaire *")

        self.email=CreatEntry(self,485,42,7,0,placeholder_text="Votre Email *",Font_size=12)
        self.email.EntryPlace(0.5,0.59,"center")

        self.password=CreatEntry(self,235,42,7,0,placeholder_text="Votre password *",Font_size=12)
        self.password.EntryPlace(0.27,0.69,"center")

        self.Confir_password=CreatEntry(self,235,42,7,0,placeholder_text="Confirmation password *",Font_size=12)
        self.Confir_password.EntryPlace(0.73,0.69,"center")
        

        self.buttonConnect=CreatButton(self,"Valide",485,35,command=self.valide_formulaire)
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
            text_color="#64748b",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5,rely=0.93,anchor="center")
        self.show_Frame()

    def on_entre(self,event):
        self.ConnecteAccount.buttonConfig(text_color="#3b82f6")
   
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
        
    def change_to_sisncrire(self):
        from Frontend.Siscrire import Apk
        self.destroy()
        manager=ChangeFrame(self.master)
        manager.show_frame(lambda parent:Apk(parent,"Enter your email","Enter your password","Stagaire.csv","Stagaire"))

    def validate_nom_prenom(self,type):
        if not type:
            messagebox.showerror("error",f"Le {type} est obligatoire.")
            return False
        if len(type) < 2:
            messagebox.showerror("error",f"Le {type} doit contenir au moins 2 caractères.")
            return False
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$',type):
            messagebox.showinfo("error",f"Le {type} contient des caractères invalides.")
            return False
        return True


    def validate_sexe(self,sexe):
        if not sexe:
            messagebox.showerror('error','Le sexe est obligatoire.')
            return False
        sexe=sexe.lower()
        if sexe not in ["homme","femme","masculin","féminin","m","f"]:
            messagebox.showerror('error',"Veuillez entrer 'Homme', 'Femme', 'M' ou 'F'.")
            return False
        return True
    
    def validate_date_naissance(self,date_str):
        if not date_str:
            messagebox.showerror('error','La date de naissance est obligatoire.')
            return False

        date_formats=["%d/%m/%Y","%d-%m-%Y"]
        
        for i in date_formats:
            try:
                date_obj=datetime.strptime(date_str,i)
                now=datetime.now()

                if date_obj > now:
                    messagebox.showerror('error','La date de naissance doit être dans le passé.')
                    return False

                age=now.year-date_obj.year-((now.month,now.day)<(date_obj.month,date_obj.day))
                if age<15:
                    messagebox.showerror('error','Vous devez avoir au moins 15 ans pour vous inscrire.')
                    return False
                
                return True
            except ValueError:
                pass
        messagebox.showerror('error','Format de date invalide. Utilisez JJ/MM/AAAA ou JJ-MM-AAAA.')
        return False


    def validate_password(self,password,confirm):

        if not password:
            messagebox.showerror('error','Le mot de passe est obligatoire.')
            return False
        
        if len(password) < 8:
            messagebox.showerror('error','Le mot de passe doit contenir au moins 8 caractères.')
            return False
        
        if not re.search(r'[A-Z]',password):
            messagebox.showerror('error','Le mot de passe doit contenir au moins une lettre majuscule.')
            return False
        
        if not re.search(r'[a-z]',password):
            messagebox.showerror('error','Le mot de passe doit contenir au moins une lettre minuscule.')
            return False
        
        if not re.search(r'[0-9]',password):
            messagebox.showerror('error','Le mot de passe doit contenir au moins un chiffre.')
            return False
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]',password):
            messagebox.showerror('error','Le mot de passe doit contenir au moins un caractère spécial.')
            return False
        if password!=confirm:
            messagebox.showerror('error','Le mot de pass ne correspond pas.')
            return False
        return True

    def validate_dropdowns(self):
        if self.Niveau.get()=="Votre Niveau scolaire *":
            messagebox.showerror("error","Veuillez sélectionner un niveau scolaire.")
            return False
        if self.Bac.get() == "Votre Année de bac *":
            messagebox.showerror("error","Veuillez sélectionner un type de Bac.")
            return False
        return True
    def validate_email(self, email):
        if not email:
            messagebox.showerror('error',"L'adresse email est obligatoire.")
            return False
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern,email):
            messagebox.showerror('error',"Format d'email invalide.")
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
            messagebox.showerror('error',f"Vouliez-vous dire {corrected_email}?")
            return False
        return True
    
    def valide_formulaire(self):
        try:
            nom = self.nom.get().strip()
            prenom = self.prenom.get().strip()
            email = self.email.get().strip()
            sexe = self.sexe.get().strip()
            password = self.password.get().strip()
            confirmPass = self.Confir_password.get().strip()
            dateNaissance = self.dateNaissance.get().strip()

            valide_nom = self.validate_nom_prenom(nom)
            valide_prenom = self.validate_nom_prenom(prenom)
            valide_email = self.validate_email(email)
            valide_password = self.validate_password(password, confirmPass)
            valide_date = self.validate_date_naissance(dateNaissance)
            valide_sexe = self.validate_sexe(sexe)
            valide_dropdown = self.validate_dropdowns()

            all_valide = [valide_email, valide_nom, valide_password, valide_prenom, valide_sexe, valide_date, valide_dropdown]

            if False not in all_valide:
                
                
                with open('utilisateurs.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Nom','Prénom','Sexe','Date de naissance','Mot de passe','Niveau','Année de bac','Email'])
                    writer.writerow([
                        nom, 
                        prenom, 
                        sexe, 
                        dateNaissance, 
                        password, 
                        self.Niveau.get().strip(), 
                        self.Bac.get().strip(),
                        email
                    ])
                messagebox.showinfo("Succès", "Inscription réussie!")
                self.change_to_accueil()
        except Exception as e:
            messagebox.showerror("Erreur système", f"Une erreur inattendue s'est produite: {str(e)}")
                    
