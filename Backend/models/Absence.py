from Backend.db.connexion import ConnexionDB

class AbsenceManager:
    def __init__(self):
        self.db = ConnexionDB()

    def enregistrer_absence(self, etudiant_id, seance_id, date_absence, duree_minutes, motif):
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO absence (etudiant_id, seance_id, date_absence, duree_minutes, motif)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (etudiant_id, seance_id, date_absence, duree_minutes, motif)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def toutes_absences(self):
        if not self.db.connecter():
            return []
        try:
            requete = "SELECT id, etudiant_id, seance_id, date_absence, justification FROM absence"
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def absences_par_etudiant(self, etudiant_id):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT a.id, a.date_absence, a.duree_minutes, a.justification,
                       s.type_seance, m.name as module
                FROM absence a
                JOIN seance s ON a.seance_id = s.id
                JOIN module m ON s.module_id = m.id
                WHERE a.etudiant_id = ?
            """
            cursor = self.db.executer(requete, (etudiant_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def absences_par_seance(self, seance_id):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT a.id, e.code_apogee, e.nom, e.prenom, a.date_absence, a.justification
                FROM absence a
                JOIN etudiant e ON a.etudiant_id = e.id
                WHERE a.seance_id = ?
            """
            cursor = self.db.executer(requete, (seance_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def absences_non_justifiees(self):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT a.id, e.code_apogee, e.nom, e.prenom, a.date_absence,
                       s.type_seance, m.name as module
                FROM absence a
                JOIN etudiant e ON a.etudiant_id = e.id
                JOIN seance s ON a.seance_id = s.id
                JOIN module m ON s.module_id = m.id
                WHERE a.justification = 0
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def justifier_absence(self, absence_id, motif, document_path):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE absence
                SET justification = 1,
                    date_justification = CURRENT_TIMESTAMP,
                    motif = ?,
                    document_path = ?
                WHERE id = ?
            """
            return self.db.executer(requete, (motif, document_path, absence_id)) is not None
        finally:
            self.db.deconnecter()

    def valider_justification_admin(self, absence_id, validee_par, commentaire):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE absence
                SET validee_par = ?,
                    commentaire = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            return self.db.executer(requete, (validee_par, commentaire, absence_id)) is not None
        finally:
            self.db.deconnecter()

    def supprimer_absence(self, absence_id):
        if not self.db.connecter():
            return False
        try:
            requete = "DELETE FROM absence WHERE id = ?"
            return self.db.executer(requete, (absence_id,)) is not None
        finally:
            self.db.deconnecter()
