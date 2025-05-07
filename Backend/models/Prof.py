from Backend.db.connexion import ConnexionDB
from Backend.utils.crypto import Crypto
from datetime import datetime

class ProfManager:
    def __init__(self):
        self.db = ConnexionDB()

    def ajouter_prof(self, cin, first_name, last_name, email, password, telephone, specialite, date_entree, filiere_id):
        """Ajoute un nouveau professeur dans la base de données."""
        if not self.db.connecter():
            return False
        try:
            hashed_password = Crypto.encrypt(password)
            requete = """
                INSERT INTO prof (cin, first_name, last_name, email, password, telephone, specialite, date_entree, filiere_principale)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (cin, first_name, last_name, email, hashed_password, telephone, specialite, date_entree, filiere_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def lister_profs_actifs(self):
        """Retourne tous les professeurs actifs."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, cin, first_name, last_name, email, specialite, status
                FROM prof
                WHERE status = 'Actif'
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def lister_profs_par_filiere(self, code_filiere):
        """Liste les professeurs liés à une filière donnée."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT p.id, p.cin, p.first_name, p.last_name, p.specialite, f.name as filiere
                FROM prof p
                JOIN filiere f ON p.filiere_principale = f.id
                WHERE f.code = ?
            """
            params = (code_filiere,)
            cursor = self.db.executer(requete, params)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def mettre_a_jour_infos(self, cin, email, telephone):
        """Met à jour les informations d'un professeur via CIN."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE prof
                SET email = ?, telephone = ?, updated_at = CURRENT_TIMESTAMP
                WHERE cin = ?
            """
            params = (email, telephone, cin)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def changer_statut(self, prof_id, nouveau_statut='Inactif'):
        """Change le statut d'un professeur (ex: actif/inactif)."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE prof
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (nouveau_statut, prof_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def supprimer_prof(self, prof_id):
        """Supprime un professeur par ID."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                DELETE FROM prof
                WHERE id = ?
            """
            params = (prof_id,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
