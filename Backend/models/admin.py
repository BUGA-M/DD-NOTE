from Backend.db.connexion import ConnexionDB
from backend.utils.crypto import Crypto
from datetime import datetime

class AdminManager:
    def __init__(self):
        self.db = ConnexionDB()
        
    def ajouter_admin(self, code, password, email_recup, is_active=1):
        if not self.db.connecter():
            return False
        
        try:
            encrypted_password = Crypto.encrypt(password)
            requete = """
                INSERT INTO admin (code, password, email_recup, is_active)
                VALUES (?, ?, ?, ?)
            """
            params = (code, encrypted_password, email_recup, is_active)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
    
    def liste_admins_actifs(self):
        if not self.db.connecter():
            return []
        
        try:
            requete = """
                SELECT id, code, email_recup, last_login
                FROM admin
                WHERE is_active = 1
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()
    
    def mettre_a_jour_dernier_login(self, code):
        if not self.db.connecter():
            return False
        
        try:
            requete = """
                UPDATE admin
                SET last_login = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                WHERE code = ?
            """
            params = (code,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
    
    def desactiver_admin(self, admin_id):
        if not self.db.connecter():
            return False
        
        try:
            requete = """
                UPDATE admin
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (admin_id,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
    
    def supprimer_admin(self, admin_id):
        if not self.db.connecter():
            return False
        
        try:
            requete = """
                DELETE FROM admin
                WHERE id = ?
            """
            params = (admin_id,)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
    
    def verifier_login(self, code, password):
        if not self.db.connecter():
            return None
        
        try:
            requete = """
                SELECT id, code, password
                FROM admin
                WHERE code = ? AND is_active = 1
            """
            params = (code,)
            cursor = self.db.executer(requete, params)
            if cursor:
                admin = cursor.fetchone()
                if admin:
                    try:
                        decrypted_password = Crypto.decrypt(admin['password'])
                        if decrypted_password == password:
                            self.mettre_a_jour_dernier_login(code)
                            return {'id': admin['id'], 'code': admin['code']}
                    except Exception:
                        return None
            return None
        finally:
            self.db.deconnecter()
    
    def recuperer_admin_par_id(self, admin_id):
        if not self.db.connecter():
            return None
        
        try:
            requete = """
                SELECT id, code, email_recup, last_login, is_active
                FROM admin
                WHERE id = ?
            """
            params = (admin_id,)
            cursor = self.db.executer(requete, params)
            return cursor.fetchone() if cursor else None
        finally:
            self.db.deconnecter()
    
    def modifier_mot_de_passe(self, admin_id, nouveau_password):
        if not self.db.connecter():
            return False
        
        try:
            encrypted_password = Crypto.encrypt(nouveau_password)
            requete = """
                UPDATE admin
                SET password = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (encrypted_password, admin_id)
            resultat = self.db.executer(requete, params)
            return resultat is not None
        finally:
            self.db.deconnecter()
