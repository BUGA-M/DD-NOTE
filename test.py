import sqlite3
import os
import hashlib
from datetime import datetime

class BaseDonnees:
    def __init__(self, db_name="dd_note.db"):
        self.db_name=db_name
        self.connection=None
        self.cursor=None
        os.makedirs(os.path.dirname(self.db_name) if os.path.dirname(self.db_name) else '.', exist_ok=True)
        self.initialiser_tables()
    
    def connecter(self):
        try:
            self.connection=sqlite3.connect(self.db_name)
            self.cursor=self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def deconnecter(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def initialiser_tables(self):
        if self.connecter():
            try:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS inscription (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL,
                        sexe TEXT NOT NULL,
                        dataNaissance TEXT NOT NULL,
                        email TEXT UNIQUE,
                        password TEXT,
                        bac TEXT NOT NULL,
                        niveau TEXT NOT NULL,
                        filiere TEXT NOT NULL,
                        verified INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS verification_codes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE,
                        code TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        token TEXT UNIQUE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        expired_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES inscription (id)
                    )
                """)
                

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        matiere TEXT NOT NULL,
                        note REAL NOT NULL,
                        coefficient REAL DEFAULT 1.0,
                        date_exam TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES inscription (id)
                    )
                """)
                
                self.commit()
            except sqlite3.Error as e:
                print(f"Erreur lors de l'initialisation des tables: {e}")
            finally:
                self.deconnecter()
    
    # Méthodes CRUD génériques
    
    def executer_requete(self,requete,parametres=None):
        try:
            if self.connecter():
                if parametres:
                    self.cursor.execute(requete,parametres)
                else:
                    self.cursor.execute(requete)
                self.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erreur d'exécution de requête: {e}")
            return False
        finally:
            self.deconnecter()
    
    def obtenir_resultat(self,requete,parametres=None,fetchall=False):
        try:
            if self.connecter():
                if parametres:
                    self.cursor.execute(requete, parametres)
                else:
                    self.cursor.execute(requete)
                
                if fetchall:
                    return self.cursor.fetchall()
                else:
                    return self.cursor.fetchone()
            return None
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de résultats: {e}")
            return None
        finally:
            self.deconnecter()
    
    # Méthodes pour la gestion des inscriptions
    
    def inserer_utilisateur(self, nom, prenom, sexe, date_naissance, email, bac, niveau, filiere):
        requete = """
        INSERT INTO inscription (nom, prenom, sexe, dataNaissance, email, bac, niveau, filiere)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        parametres = (nom, prenom, sexe, date_naissance, email, bac, niveau, filiere)
        """Returns:
            bool: True si l'insertion a réussi, False sinon"""
        return self.executer_requete(requete, parametres)
    
    def mettre_a_jour_mot_de_passe(self,email,mot_de_passe):
        requete = """
        UPDATE inscription SET password = ?, verified = 1 WHERE email = ?
        """
        parametres = (mot_de_passe,email)
        return self.executer_requete(requete, parametres)
    
    def verifier_login(self, email, mot_de_passe):
        requete = """
        SELECT id, nom, prenom, email FROM inscription 
        WHERE email = ? AND password = ? AND verified = 1
        """
        parametres = (email, mot_de_passe)
        """Données de l'utilisateur si connexion réussie, None sinon"""
        return self.obtenir_resultat(requete, parametres)
    
    def obtenir_utilisateur_par_email(self, email):
        """
            Returns: Données de l'utilisateur ou None si non trouvé
        """
        requete = "SELECT * FROM inscription WHERE email = ?"
        parametres = (email,)
        return self.obtenir_resultat(requete, parametres)
    
    def email_existe(self, email):
        """            
        Returns:
            bool: True si l'email existe, False sinon
        """
        requete = "SELECT 1 FROM inscription WHERE email = ?"
        parametres = (email,)
        resultat = self.obtenir_resultat(requete, parametres)
        return resultat is not None
    
    def supprimer_utilisateur(self, email):
        """            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        requete = "DELETE FROM inscription WHERE email = ?"
        parametres = (email,)
        return self.executer_requete(requete, parametres)
    
    
    def enregistrer_code_verification(self,email,code):
        """
        Enregistre un code de vérification pour un email.
        
        Args:
            email (str): Email de l'utilisateur
            code (str): Code de vérification
            
        Returns:
            bool: True si l'enregistrement a réussi, False sinon
        """
        requete = """
        INSERT OR REPLACE INTO verification_codes (email, code, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """
        parametres = (email, code)
        return self.executer_requete(requete, parametres)
    
    def obtenir_code_verification(self, email):
        """
        Récupère le code de vérification pour un email.
        
        Args:
            email (str): Email de l'utilisateur
            
        Returns:
            str: Code de vérification ou None si non trouvé
        """
        requete = """
        SELECT code FROM verification_codes 
        WHERE email = ? AND datetime(timestamp, '+5 minutes') > datetime('now')
        """
        parametres = (email,)
        resultat = self.obtenir_resultat(requete, parametres)
        return resultat[0] if resultat else None
    
    def supprimer_code_verification(self, email):
        """
        Supprime le code de vérification pour un email.
        
        Args:
            email (str): Email de l'utilisateur
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        requete = "DELETE FROM verification_codes WHERE email = ?"
        parametres = (email,)
        return self.executer_requete(requete, parametres)
    
    def nettoyer_codes_expires(self):
        """
        Supprime tous les codes de vérification expirés (plus de 5 minutes).
        
        Returns:
            bool: True si le nettoyage a réussi, False sinon
        """
        requete = "DELETE FROM verification_codes WHERE datetime(timestamp, '+5 minutes') < datetime('now')"
        return self.executer_requete(requete)
    
    # Méthodes pour la gestion des sessions
    
    def creer_session(self, user_id, duree_heures=24):
        """
        Crée une nouvelle session pour un utilisateur.
        
        Args:
            user_id (int): ID de l'utilisateur
            duree_heures (int): Durée de validité de la session en heures
            
        Returns:
            str: Token de session ou None si échec
        """
        import uuid
        
        # Générer un token unique
        token = str(uuid.uuid4())
        
        requete = """
        INSERT INTO sessions (user_id, token, expired_at)
        VALUES (?, ?, datetime('now', '+? hours'))
        """
        parametres = (user_id, token, duree_heures)
        
        if self.executer_requete(requete, parametres):
            return token
        return None
    
    def verifier_session(self, token):
        """
        Vérifie si une session est valide.
        
        Args:
            token (str): Token de session
            
        Returns:
            int: ID de l'utilisateur si session valide, None sinon
        """
        requete = """
        SELECT user_id FROM sessions
        WHERE token = ? AND datetime(expired_at) > datetime('now')
        """
        parametres = (token,)
        resultat = self.obtenir_resultat(requete, parametres)
        return resultat[0] if resultat else None
    
    def supprimer_session(self, token):
        """
        Supprime une session (déconnexion).
        
        Args:
            token (str): Token de session
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        requete = "DELETE FROM sessions WHERE token = ?"
        parametres = (token,)
        return self.executer_requete(requete, parametres)
    
    
    def ajouter_note(self, user_id, matiere, note, coefficient, date_exam):
        """
        Ajoute une note pour un étudiant.
        
        Args:
            user_id (int): ID de l'utilisateur
            matiere (str): Nom de la matière
            note (float): Note obtenue
            coefficient (float): Coefficient de la matière
            date_exam (str): Date de l'examen au format JJ/MM/AAAA
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        requete = """
        INSERT INTO notes (user_id, matiere, note, coefficient, date_exam)
        VALUES (?, ?, ?, ?, ?)
        """
        parametres = (user_id, matiere, note, coefficient, date_exam)
        return self.executer_requete(requete, parametres)
    
    def obtenir_notes_par_utilisateur(self, user_id):
        """
        Récupère toutes les notes d'un utilisateur.
        
        Args:
            user_id (int): ID de l'utilisateur
            
        Returns:
            list: Liste des notes ou liste vide si aucune note
        """
        requete = """
        SELECT id, matiere, note, coefficient, date_exam 
        FROM notes WHERE user_id = ? 
        ORDER BY date_exam DESC
        """
        parametres = (user_id,)
        resultat = self.obtenir_resultat(requete, parametres, fetchall=True)
        return resultat if resultat else []
    
    def calculer_moyenne(self, user_id):
        """
        Calcule la moyenne pondérée des notes d'un utilisateur.
        
        Args:
            user_id (int): ID de l'utilisateur
            
        Returns:
            float: Moyenne pondérée ou None si aucune note
        """
        requete = """
        SELECT SUM(note * coefficient) / SUM(coefficient) as moyenne
        FROM notes WHERE user_id = ?
        """
        parametres = (user_id,)
        resultat = self.obtenir_resultat(requete, parametres)
        return resultat[0] if resultat and resultat[0] is not None else None
    
    def modifier_note(self, note_id, matiere, note, coefficient, date_exam):
        """
        Modifie une note existante.
        
        Args:
            note_id (int): ID de la note à modifier
            matiere (str): Nom de la matière
            note (float): Note obtenue
            coefficient (float): Coefficient de la matière
            date_exam (str): Date de l'examen au format JJ/MM/AAAA
            
        Returns:
            bool: True si la modification a réussi, False sinon
        """
        requete = """
        UPDATE notes 
        SET matiere = ?, note = ?, coefficient = ?, date_exam = ?
        WHERE id = ?
        """
        parametres = (matiere, note, coefficient, date_exam, note_id)
        return self.executer_requete(requete, parametres)
    
    def supprimer_note(self, note_id):
        """
        Supprime une note.
        
        Args:
            note_id (int): ID de la note à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        requete = "DELETE FROM notes WHERE id = ?"
        parametres = (note_id,)
        return self.executer_requete(requete, parametres)

    # Méthodes pour la migration des données
    
# Initialisation de la base de données
db = BaseDonnees("dd_note.db")

# Inscription d'un utilisateur
db.inserer_utilisateur(
    nom="Dupont", 
    prenom="Jean", 
    sexe="M", 
    date_naissance="01/01/2000", 
    email="jean.dupont@example.com", 
    bac="2020", 
    niveau="BAC+2", 
    filiere="Informatique"
)

# Enregistrement d'un code OTP
db.enregistrer_code_verification("jean.dupont@example.com", "123456")

# Vérification du code
code = db.obtenir_code_verification("jean.dupont@example.com")
if code == "123456":
    # Générer et enregistrer un mot de passe
    db.mettre_a_jour_mot_de_passe("jean.dupont@example.com", "mot_de_passe_securise")

# Connexion
user = db.verifier_login("jean.dupont@example.com", "mot_de_passe_securise")
if user:
    user_id = user[0]
    # Créer une session
    token = db.creer_session(user_id)
    
    # Ajouter une note
    db.ajouter_note(user_id, "Mathématiques", 16.5, 2.0, "15/04/2025")
    
    # Calculer la moyenne
    moyenne = db.calculer_moyenne(user_id)
    print(f"Moyenne: {moyenne}")