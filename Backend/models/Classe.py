from Backend.db.connexion import ConnexionDB
from datetime import datetime

class ClasseManager:
    def __init__(self):
        self.db = ConnexionDB()

    def ajouter_classe(self, name, niveau, annee_academique, filiere_id, responsable_id, capacite, salle_principale):
        """Ajoute une nouvelle classe dans la base de données."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO classe (name, niveau, annee_academique, filiere_id, responsable_id, capacite, salle_principale)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (name, niveau, annee_academique, filiere_id, responsable_id, capacite, salle_principale)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def lister_classes_actives(self):
        """Retourne toutes les classes actives."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, name, niveau, annee_academique, capacite
                FROM classe
                WHERE is_active = 1
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def lister_classes_detaillees(self):
        """Retourne les classes avec nom de la filière et du responsable."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT c.id, c.name, c.niveau, c.annee_academique, f.name as filiere,
                       p.first_name || ' ' || p.last_name as responsable
                FROM classe c
                JOIN filiere f ON c.filiere_id = f.id
                LEFT JOIN prof p ON c.responsable_id = p.id
                WHERE c.is_active = 1
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def classes_par_annee(self, annee_academique):
        """Retourne les classes pour une année académique spécifique."""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT c.id, c.name, c.niveau, f.name as filiere
                FROM classe c
                JOIN filiere f ON c.filiere_id = f.id
                WHERE c.annee_academique = ?
            """
            params = (annee_academique,)
            cursor = self.db.executer(requete, params)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def mettre_a_jour_classe(self, classe_id, salle_principale, capacite):
        """Met à jour une classe (salle et capacité)."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE classe
                SET salle_principale = ?, capacite = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (salle_principale, capacite, classe_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def changer_responsable(self, classe_id, nouveau_responsable_id):
        """Change le responsable d'une classe."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE classe
                SET responsable_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (nouveau_responsable_id, classe_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def desactiver_classe(self, classe_id):
        """Désactive une classe (is_active = 0)."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE classe
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (classe_id,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()

    def supprimer_classe(self, classe_id):
        """Supprime une classe définitivement."""
        if not self.db.connecter():
            return False
        try:
            requete = """
                DELETE FROM classe
                WHERE id = ?
            """
            params = (classe_id,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
