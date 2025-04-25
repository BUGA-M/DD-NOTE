import smtplib
from email.message import EmailMessage
import ssl
import random
import customtkinter as ctk
from tkinter import messagebox
from Custom import CreatLabel, CreatEntry, CreatButton, CreatFrame, CreatComboBox, FontInstaller, ChangeFrame,CreateImage,ThemeControls,ThemeManager,ThemeColors
from Frontend.connexion import ConnexionFrame
import csv, re, os

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
    def __init__(self, master, NameDateBase, type, email=None):
        self.theme_name = ThemeManager.load_theme_preference()["color_theme"]
        self.theme_data = ThemeColors.load_colors(self.theme_name)
        super().__init__(master, 450, 450, "transparent", self.theme_data["button"], 20)
        self.type = type
        self.datebase = NameDateBase
        self.email = email
        self.title_font = FontInstaller.get_font("Titan One")
        self.subtitle_font = FontInstaller.get_font("Poppins")
        self.type_font = FontInstaller.get_font("Orbitron")
        self.CreatInterfacePass()

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
        self.buttonConnect.buttonConfig(font=(self.type_font, 14, "bold"), command="",fg_color=self.theme_data["title"])

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

    # def valide_password(self):
    #     try:
    #         password = self.NouvPassword.get().strip()
    #         conf_password = self.Confirmation_Password.get().strip()
            
    #         if not password or not conf_password:
    #             messagebox.showerror('Erreur', 'Veuillez remplir tous les champs.')
    #             return
                
    #         # Validate the passwords
    #         if validate_password(password, conf_password):
    #             # If validation passes, update password in database
    #             if self.update_password(password):
    #                 messagebox.showinfo('Succès', 'Le mot de passe a été modifié avec succès.')
                    
    #                 # Just refocus the window for now
                        
    #                 # Clear the input fields
    #                 self.NouvPassword.delete(0, 'end')
    #                 self.Confirmation_Password.delete(0, 'end')
                    
    #     except (InvalidPasswordException, StrongPasswordException) as e:
    #         # These exceptions already show their own error messages
    #         pass
    #     except Exception as e:
    #         messagebox.showerror('Erreur', f'Une erreur est survenue: {str(e)}')

    # def update_password(self, new_password):
    #     try:
    #         # Read the current database
    #         users = []
    #         found = False
            
    #         if os.path.exists(self.datebase):
    #             with open(self.datebase, 'r', newline='') as file:
    #                 reader = csv.reader(file)
    #                 header = next(reader)  # Save the header
                    
    #                 for row in reader:
    #                     if len(row) >= 2:  # Make sure the row has enough columns
    #                         # Assuming email is in the first column and password in the second
    #                         if self.email and row[0] == self.email:
    #                             # Found the user, update the password
    #                             row[1] = new_password
    #                             found = True
    #                         users.append(row)
            
    #         if not found and self.email:
    #             # If this is a new user or email wasn't found
    #             messagebox.showerror('Erreur', "Utilisateur non trouvé.")
    #             return False
                
    #         # Write back to the database
    #         with open(self.datebase, 'w', newline='') as file:
    #             writer = csv.writer(file)
    #             writer.writerow(header)  # Write the header back
    #             writer.writerows(users)
                
    #         return True
            
    #     except Exception as e:
    #         messagebox.showerror('Erreur', f"Impossible de mettre à jour le mot de passe: {str(e)}")
    #         return False
    
    def show_Frame(self):
        self.FramePlace(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    window = ctk.CTk()
    window.geometry("1280x720")
    window.minsize(500, 720)
    window.title("DDnote")
    window.config(bg="#1e293b")
    
    # For testing, you can provide an email
    app = CreatChangePassword(window, "test.csv", "proof", email="test@example.com")
    
    window.mainloop()