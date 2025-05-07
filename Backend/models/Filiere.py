from Backend.db.connexion import ConnexionDB
from datetime import datetime

class FiliereManager:
    def __init__(self):
        self.db = ConnexionDB()

    def creer_filiere(self, code, name, level, description, parent_id=None):
        """Ajoute une nouvelle filière ou sous-filière."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO filiere (code, name, level, description, parent_id)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (code, name, level, description, parent_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def lister_filieres_actives(self):
        """Retourne toutes les filières actives."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, code, name, level
                FROM filiere
                WHERE is_active = 1
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def obtenir_filiere_avec_sous_filieres(self, code):
        """Retourne une filière et ses sous-filières."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT f.id, f.code, f.name, f.level,
                       sf.id as sous_filiere_id, sf.code as sous_filiere_code
                FROM filiere f
                LEFT JOIN filiere sf ON f.id = sf.parent_id
                WHERE f.code = ?
            """
            params = (code,)
            cursor = self.db.executer(requete, params)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def mettre_a_jour_filiere(self, code, new_name, new_description):
        """Met à jour le nom et la description d'une filière."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE filiere
                SET name = ?, description = ?
                WHERE code = ?
            """
            params = (new_name, new_description, code)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def desactiver_filiere(self, filiere_id):
        """Désactive une filière (soft delete)."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE filiere
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (filiere_id,)
            resultat =
