# Backend/Managers/prof_module_manager.py

from Backend.db.connexion import ConnexionDB

class ProfModuleManager:
    def __init__(self):
        self.db = ConnexionDB()

    def attribuer_module(self, prof_id, module_id, est_responsable, heures_attribuees):
        """Attribue un module à un professeur"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO prof_module (prof_id, module_id, est_responsable, heures_attribuees)
                VALUES (?, ?, ?, ?)
            """
            params = (prof_id, module_id, est_responsable, heures_attribuees)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def modules_par_professeur(self, prof_id):
        """Récupère les modules attribués à un professeur"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT m.id, m.code, m.name, pm.est_responsable, pm.heures_attribuees
                FROM prof_module pm
                JOIN module m ON pm.module_id = m.id
                WHERE pm.prof_id = ?
            """
            cursor = self.db.executer(requete, (prof_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def professeurs_par_module(self, module_id):
        """Récupère les professeurs associés à un module"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT p.id, p.first_name || ' ' || p.last_name AS professeur, pm.est_responsable, pm.heures_attribuees
                FROM prof_module pm
                JOIN prof p ON pm.prof_id = p.id
                WHERE pm.module_id = ?
            """
            cursor = self.db.executer(requete, (module_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def maj_heures_attribuees(self, prof_id, module_id, nouvelles_heures):
        """Met à jour les heures attribuées à un professeur pour un module"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE prof_module
                SET heures_attribuees = ?, est_responsable = est_responsable, updated_at = CURRENT_TIMESTAMP
                WHERE prof_id = ? AND module_id = ?
            """
            params = (nouvelles_heures, prof_id, module_id)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def supprimer_attribution(self, prof_id, module_id):
        """Supprime l'attribution d'un module à un professeur"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                DELETE FROM prof_module
                WHERE prof_id = ? AND module_id = ?
            """
            return self.db.executer(requete, (prof_id, module_id)) is not None
        finally:
            self.db.deconnecter()
