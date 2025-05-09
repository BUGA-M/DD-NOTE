import re
from datetime import datetime
from tkinter import messagebox

class Validation:
    @staticmethod
    def validate_nom_prenom(valeur, champ_nom):
        """
        Valide un nom ou prénom
        Retourne la valeur si valide, sinon None
        """
        if not valeur:
            messagebox.showerror("Erreur", f"Le {champ_nom} est obligatoire.")
            return None
        
        valeur = valeur.strip()
        
        if len(valeur) < 2:
            messagebox.showerror("Erreur", f"Le {champ_nom} doit contenir au moins 2 caractères.")
            return None
            
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$', valeur):
            messagebox.showerror("Erreur", f"Le {champ_nom} contient des caractères invalides.")
            return None
            
        return valeur

    @staticmethod
    def validate_email(email):
        """
        Valide l'adresse email
        Retourne l'email si valide, sinon None
        """
        if not email:
            messagebox.showerror('Erreur', "L'adresse email est obligatoire.")
            return None
            
        email = email.strip().lower()
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            messagebox.showerror('Erreur', "Format d'email invalide.")
            return None

        # Vérification des domaines couramment mal orthographiés
        common_domains = {
            'gmail.co': 'gmail.com',
            'gmail.fr': 'gmail.com',
            'gmial.com': 'gmail.com',
            'gamil.com': 'gmail.com',
            'yahooo.com': 'yahoo.com',
            'yaho.com': 'yahoo.com',
            'hotmial.com': 'hotmail.com',
            'hotmil.com': 'hotmail.com',
            'outook.com': 'outlook.com'
        }
        
        username, domain = email.split('@')
        if domain in common_domains:
            corrected_domain = common_domains[domain]
            corrected_email = f"{username}@{corrected_domain}"
            messagebox.showerror('Erreur', f"Vouliez-vous dire {corrected_email}?")
            return None
            
        return email
        
    @staticmethod
    def validate_niveau_scolaire(niveau):
        """
        Valide le niveau scolaire
        Retourne la valeur si valide, sinon None
        """
        if not niveau or niveau == "Votre Niveau scolaire *":
            messagebox.showerror("Erreur", "Veuillez sélectionner un niveau scolaire.")
            return None
            
        niveau = niveau.strip()
        
        niveaux_valides = ["6éme année primaire", "3ème année collége", "Niveau Bac", "Baccalauréat"]
        
        if niveau not in niveaux_valides:
            messagebox.showerror("Erreur", "Niveau scolaire non reconnu.")
            return None
            
        return niveau
    
    @staticmethod
    def validate_date_naissance(date_str):
        """
        Valide la date de naissance
        Retourne la date au format YYYY-MM-DD si valide, sinon None
        """
        if not date_str:
            messagebox.showerror('Erreur', 'La date de naissance est obligatoire.')
            return None
            
        date_str = date_str.strip()
        date_formats = ["%d/%m/%Y", "%d-%m-%Y"]
        
        for date_format in date_formats:
            try:
                date_obj = datetime.strptime(date_str, date_format)
                now = datetime.now()

                if date_obj > now:
                    messagebox.showerror('Erreur', 'La date de naissance doit être dans le passé.')
                    return None

                age = now.year - date_obj.year - ((now.month, now.day) < (date_obj.month, date_obj.day))
                if age < 15:
                    messagebox.showerror('Erreur', 'Vous devez avoir au moins 15 ans pour vous inscrire.')
                    return None
                
                # Retourner au format YYYY-MM-DD pour la base de données
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue
                
        messagebox.showerror('Erreur', 'Format de date invalide. Utilisez JJ/MM/AAAA ou JJ-MM-AAAA.')
        return None

    @staticmethod
    def validate_sexe(sexe):
        """
        Valide le sexe
        Retourne le sexe normalisé si valide, sinon None
        """
        if not sexe:
            messagebox.showerror('Erreur', 'Le sexe est obligatoire.')
            return None
            
        sexe = sexe.strip().lower()
        
        if sexe not in ['homme', 'femme']:
            messagebox.showerror('Erreur', "Veuillez entrer 'Homme' ou 'Femme'")
            return None
            
        # Normaliser avec première lettre en majuscule
        return sexe.capitalize()

    @staticmethod
    def validate_filiere(filiere):
        """
        Valide la filière
        Retourne la valeur si valide, sinon None
        """
        if not filiere or filiere == "Votre Filiéres *":
            messagebox.showerror("Erreur", "Veuillez sélectionner une filière.")
            return None
            
        filiere = filiere.strip()
        
        # Liste des filières valides
        filieres_valides = filieres = [
            "gestion hôtelière", "génie civil", "électromécanique", "mécanique",
            "électricité", "gestion", "tourisme", "btp (bâtiment et travaux publics)",
            "développement digital", "réseaux informatiques", "pâtisserie",
            "métiers de la coiffure et esthétique", "plomberie sanitaire",
            "menuiserie aluminium et bois", "développement informatique",
            "génie électrique", "agroalimentaire", "biotechnologie",
            "maintenance industrielle", "design graphique", "mécatronique",
            "gestion des entreprises", "finance-comptabilité", "commerce international",
            "secrétariat", "communication", "éducation préscolaire"
        ]

        
        if filiere not in filieres_valides:
            messagebox.showerror("Erreur", "Filière non reconnue.")
            return None
            
        return filiere

    @staticmethod
    def validate_Typebac(bac_str):
        """
        Valide le type de bac
        Retourne la valeur si valide, sinon None
        """
        if not bac_str or bac_str == "Votre type de BAC":
            messagebox.showerror('Erreur', 'Le type de bac est obligatoire.')
            return None
            
        bac_str = bac_str.strip()
        
        # Liste des types de bac valides
        bacs_valides = [
            "Pas de Bac",
            "Sciences Mathématiques A",
            "Sciences Mathématiques B",
            "Sciences Physiques",
            "Sciences de la Vie et de la Terre",
            "Sciences Agronomiques",
            "Sciences et Technologies Électriques",
            "Sciences et Technologies Mécaniques",
            "Arts Appliqués",
            "Sciences Économiques",
            "Sciences de Gestion Comptable",
            "Lettres",
            "Sciences Humaines",
            "Sciences Islamiques",
            "2ème Bac Sciences Mathématiques A (BIOF)",
            "2ème Bac Sciences Mathématiques B (BIOF)",
            "2ème Bac Sciences Physiques (BIOF)",
            "2ème Bac Sciences de la Vie et de la Terre (SVT) (BIOF)",
            "2ème Bac Sciences Agronomiques (BIOF)",
            "2ème Bac Sciences et Technologies Électriques (BIOF)",
            "2ème Bac Sciences et Technologies Mécaniques (BIOF)"
        ]
        
        try: 
            if bac_str not in bacs_valides:
                messagebox.showerror('Erreur', 'Type de bac non reconnu.')
                return None
        except Exception as e:
            print(f"[Erreur Test Bac]: {e}")
            return None
              
        return bac_str

    @staticmethod
    def validate_bac_year(year_str):
        """
        Valide l'année du bac
        Retourne l'année en entier si valide, sinon None
        """
        if not year_str:
            messagebox.showerror('Erreur', 'L\'année du bac est obligatoire.')
            return None
            
        year_str = year_str.strip()
        
        try:
            year = int(year_str)
            current_year = datetime.now().year
            
            if 2013 <= year <= current_year + 1:  # Permet l'année suivante pour les inscriptions anticipées
                return year
            else:
                messagebox.showerror('Erreur', f'L\'année du bac doit être entre 2013 et {current_year + 1}.')
                return None
        except ValueError:
            messagebox.showerror('Erreur', 'Format invalide. Entrez une année valide (ex: 2018).')
            return None
    

    @staticmethod
    def validate_telephone(telephone):
        """
        Valide un numéro de téléphone
        Retourne le numéro si valide, sinon None
        """
        if not telephone:  # Le téléphone peut être facultatif
            return ""
            
        telephone = telephone.strip()
        
        # Supprimer les espaces, tirets et autres caractères non numériques
        telephone_clean = ''.join(filter(str.isdigit, telephone))
        
        # Vérifier la longueur
        if len(telephone_clean) < 10 or len(telephone_clean) > 15:
            messagebox.showerror('Erreur', "Le numéro de téléphone doit contenir entre 10 et 15 chiffres.")
            return None
            
        # Format international avec le + si nécessaire
        if telephone.startswith('+'):
            return f"+{telephone_clean}"
        else:
            return telephone_clean

    @staticmethod
    def validate_password(password, confirm_password=None):
        """
        Valide un mot de passe
        Retourne le mot de passe si valide, sinon None
        """
        if not password:
            messagebox.showerror('Erreur', "Le mot de passe est obligatoire.")
            return None
            
        if len(password) < 8:
            messagebox.showerror('Erreur', "Le mot de passe doit contenir au moins 8 caractères.")
            return None
            
        if not re.search(r'[A-Z]', password):
            messagebox.showerror('Erreur', "Le mot de passe doit contenir au moins une lettre majuscule.")
            return None
            
        if not re.search(r'[a-z]', password):
            messagebox.showerror('Erreur', "Le mot de passe doit contenir au moins une lettre minuscule.")
            return None
            
        if not re.search(r'[0-9]', password):
            messagebox.showerror('Erreur', "Le mot de passe doit contenir au moins un chiffre.")
            return None
            
        if confirm_password is not None and password != confirm_password:
            messagebox.showerror('Erreur', "Les mots de passe ne correspondent pas.")
            return None
            
        return password

    @staticmethod
    def validate_moyenne_bac(moyenne_str):
        """
        Valide la moyenne du bac
        Retourne la moyenne en float si valide, sinon None
        """
        if not moyenne_str:  # La moyenne peut être facultative
            return None
            
        moyenne_str = moyenne_str.strip().replace(',', '.')
        
        try:
            moyenne = float(moyenne_str)
            
            if 0 <= moyenne <= 20:
                return moyenne
            else:
                messagebox.showerror('Erreur', "La moyenne du bac doit être comprise entre 0 et 20.")
                return None
        except ValueError:
            messagebox.showerror('Erreur', "Format de moyenne invalide. Utilisez un nombre (ex: 14.5).")
            return None

    @staticmethod
    def validate_adresse(adresse):
        """
        Valide une adresse
        Retourne l'adresse si valide, sinon une chaîne vide
        """
        # L'adresse est facultative, donc retourner une chaîne vide si non fournie
        if not adresse:
            return ""
            
        adresse = adresse.strip()
        
        if len(adresse) < 5:
            messagebox.showwarning('Attention', "L'adresse semble trop courte.")
            
        return adresse