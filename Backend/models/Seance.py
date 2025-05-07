# Backend/Managers/seance_manager.py

from Backend.db.connexion import ConnexionDB

class SeanceManager:
    def __init__(self):
        self.db = ConnexionDB()

    def planifier_seance(self, volume_horaire, date_heure, heure_fin, salle, type_seance, prof_id, module_id, classe_id, sujet):
        """Ajoute une nouvelle séance planifiée"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO seance (volume_horaire, date_heure, heure_fin, salle, type_seance,
                                    prof_id, module_id, classe_id, sujet)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (volume_horaire, date_heure, heure_fin, salle, type_seance,
                      prof_id, module_id, classe_id, sujet)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def toutes_seances_planifiees(self):
        """Retourne toutes les séances ayant le statut 'Planifié'"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, date_heure, heure_fin, salle, type_seance, statut
                FROM seance
                WHERE statut = 'Planifié'
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def seances_par_prof(self, prof_id):
        """Retourne les séances d'un professeur"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT s.id, s.date_heure, s.heure_fin, s.salle, s.type_seance, m.name as module, c.name as classe
                FROM seance s
                JOIN module m ON s.module_id = m.id
                JOIN classe c ON s.classe_id = c.id
                WHERE s.prof_id = ?
            """
            cursor = self.db.executer(requete, (prof_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def seances_par_module(self, module_id):
        """Retourne les séances d'un module"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT s.id, s.date_heure, s.heure_fin, s.salle, s.type_seance,
                       p.first_name || ' ' || p.last_name as professeur
                FROM seance s
                JOIN prof p ON s.prof_id = p.id
                WHERE s.module_id = ?
            """
            cursor = self.db.executer(requete, (module_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def seances_par_classe(self, classe_id):
        """Retourne les séances d'une classe"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT s.id, s.date_heure, s.heure_fin, s.salle, s.type_seance,
                       m.name as module, p.first_name || ' ' || p.last_name as professeur
                FROM seance s
                JOIN module m ON s.module_id = m.id
                JOIN prof p ON s.prof_id = p.id
                WHERE s.classe_id = ?
            """
            cursor = self.db.executer(requete, (classe_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def seances_dans_periode(self, date_debut, date_fin):
        """Retourne les séances dans une période donnée"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, date_heure, heure_fin, salle, type_seance, module_id, classe_id
                FROM seance
                WHERE date_heure BETWEEN ? AND ?
            """
            cursor = self.db.executer(requete, (date_debut, date_fin))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def mise_a_jour_seance(self, seance_id, salle, date_heure, heure_fin):
        """Met à jour la date, heure et salle d'une séance"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE seance
                SET salle = ?, date_heure = ?, heure_fin = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            return self.db.executer(requete, (salle, date_heure, heure_fin, seance_id)) is not None
        finally:
            self.db.deconnecter()

    def changer_statut(self, seance_id, nouveau_statut):
        """Change le statut d'une séance"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE seance
                SET statut = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            return self.db.executer(requete, (nouveau_statut, seance_id)) is not None
        finally:
            self.db.deconnecter()

    def valider_pa r_admin(self, seance_id, validateur_id):
        """Valide une séance par un admin"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE seance
                SET validation_admin = 1, validateur_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            return self.db.executer(requete, (validateur_id, seance_id)) is not None
        finally:
            self.db.deconnecter()

    def supprimer_seance(self, seance_id):
        """Supprime une séance"""
        if not self.db.connecter():
            return False
        try:
            requete = "DELETE FROM seance WHERE id = ?"
            return self.db.executer(requete, (seance_id,)) is not None
        finally:
            self.db.deconnecter()
