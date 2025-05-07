from Backend.db.connexion import ConnexionDB

class ModuleManager:
    def __init__(self):
        self.db = ConnexionDB()

    def ajouter_module(self, code, name, description, volume_horaire, heures_cm, heures_td, heures_tp, semestre, coefficient, filiere_id, prof_id):
        if not self.db.connecter():
            return False
        try:
            requete = """
                INSERT INTO module (code, name, description, volume_horaire, heures_cm, heures_td, heures_tp, semestre, coefficient, filiere_id, prof_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (code, name, description, volume_horaire, heures_cm, heures_td, heures_tp, semestre, coefficient, filiere_id, prof_id)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def liste_modules(self):
        if not self.db.connecter():
            return []
        try:
            requete = "SELECT id, code, name, volume_horaire, semestre, coefficient FROM module"
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def modules_par_filiere(self, code_filiere):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT m.id, m.code, m.name, m.semestre, f.name as filiere
                FROM module m
                JOIN filiere f ON m.filiere_id = f.id
                WHERE f.code = ?
            """
            cursor = self.db.executer(requete, (code_filiere,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def modules_par_prof(self, prof_id):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT m.id, m.code, m.name, m.semestre, p.first_name || ' ' || p.last_name as responsable
                FROM module m
                JOIN prof p ON m.prof_id = p.id
                WHERE p.id = ?
            """
            cursor = self.db.executer(requete, (prof_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def modifier_module(self, code, new_name, new_description):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE module
                SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE code = ?
            """
            params = (new_name, new_description, code)
            return self.db.executer(requete, params) is not None
        finally:
            self.db.deconnecter()

    def changer_prof_responsable(self, module_id, new_prof_id):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE module
                SET prof_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            return self.db.executer(requete, (new_prof_id, module_id)) is not None
        finally:
            self.db.deconnecter()

    def supprimer_module(self, module_id):
        if not self.db.connecter():
            return False
        try:
            requete = "DELETE FROM module WHERE id = ?"
            return self.db.executer(requete, (module_id,)) is not None
        finally:
            self.db.deconnecter()
