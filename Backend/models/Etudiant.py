from Backend.db.connexion import ConnexionDB
from Backend.utils.crypto import Crypto
from datetime import datetime

class EtudiantManager:
    def __init__(self):
        self.db = ConnexionDB()
    
    def email_existe(self, email):
        if not self.db.connecter():
            return False
        try:
            requete = "SELECT 1 FROM etudiant WHERE email = ? LIMIT 1"
            cursor = self.db.executer(requete, (email,))
            return cursor.fetchone() is not None
        finally:
            self.db.deconnecter()
    
    def inscrire_etudiant(self, code_apogee, nom, prenom, email, password, niveau_scolaire, date_naissance,
                          telephone, adresse, bac, moyenne_bac, classe_id, filiere_nom):
        if not self.db.connecter():
            return False
        try:
            password_chiffre = Crypto.encrypt(password)
            requete = """
                INSERT INTO etudiant (
                    code_apogee, nom, prenom, email, password, niveau_scolaire, date_naissance,
                    telephone, adresse, bac, moyenne_bac, classe_id, filiere_nom
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                code_apogee, nom, prenom, email, password_chiffre, niveau_scolaire, date_naissance,
                telephone, adresse, bac, moyenne_bac, classe_id, filiere_nom
            )
            self.db.executer(requete, params)
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Inscription étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def get_etudiants_actifs(self):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, code_apogee, nom, prenom, email, filiere_nom, statut
                FROM etudiant
                WHERE statut = 'Actif'
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_en_attente(self):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, code_apogee, nom, prenom, email, filiere_nom, bac, moyenne_bac
                FROM etudiant
                WHERE validation_admin = 0
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_par_classe(self, nom_classe):
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT e.id, e.code_apogee, e.nom, e.prenom, e.email, c.name as classe
                FROM etudiant e
                JOIN classe c ON e.classe_id = c.id
                WHERE c.name = ? AND e.statut = 'Actif'
            """
            cursor = self.db.executer(requete, (nom_classe,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def valider_etudiant(self, etudiant_id):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET validation_admin = 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(requete, (etudiant_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Validation étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def maj_infos_etudiant(self, code_apogee, email, telephone, adresse):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET email = ?, telephone = ?, adresse = ?, updated_at = CURRENT_TIMESTAMP
                WHERE code_apogee = ?
            """
            self.db.executer(requete, (email, telephone, adresse, code_apogee))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] MAJ infos étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def changer_classe_etudiant(self, etudiant_id, nouvelle_classe_id):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET classe_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(requete, (nouvelle_classe_id, etudiant_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Changement de classe étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def changer_statut_etudiant(self, etudiant_id, nouveau_statut):
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET statut = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(requete, (nouveau_statut, etudiant_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Changement de statut étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def supprimer_etudiant(self, etudiant_id):
        if not self.db.connecter():
            return False
        try:
            requete = "DELETE FROM etudiant WHERE id = ?"
            self.db.executer(requete, (etudiant_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Suppression étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()
