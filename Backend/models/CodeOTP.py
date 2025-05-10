from Backend.db.connexion import ConnexionDB

class CodeVerificationManager:
    def __init__(self):
        self.db = ConnexionDB()

    def enregistrer_code(self, email, code, type_code='activation', expire_minutes=5):
        if not self.db.connecter():
            return False
        try:
            delete_old = """
            DELETE FROM code_verification
            WHERE email = ? AND type = ? AND verifie = 0;
            """
            self.db.executer(delete_old, (email, type_code))

            requete = """
            INSERT INTO code_verification (email, code, type, expire_at, date_envoi)
            VALUES (?, ?, ?, DATETIME('now', '+' || ? || ' minutes'), DATETIME('now'));
            """
            self.db.executer(requete, (email, code, type_code, expire_minutes))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Enregistrement code : {e}")
            return False
        finally:
            self.db.deconnecter()

    def get_code(self, email, type_code='activation'):
        if not self.db.connecter():
            return None
        try:
            requete = """
            SELECT code FROM code_verification
            WHERE email = ? AND type = ? AND verifie = 0 AND expire_at > DATETIME('now')
            ORDER BY date_envoi DESC
            LIMIT 1;
            """
            cursor = self.db.executer(requete, (email, type_code))
            resultat = cursor.fetchone()
            return resultat[0] if resultat else None
        except Exception as e:
            print(f"[ERREUR] Récupération code : {e}")
            return None
        finally:
            self.db.deconnecter()

    def verifier_code(self, email, code, type_code='activation'):
        if not self.db.connecter():
            return False
        try:
            requete = """
            SELECT * FROM code_verification
            WHERE email = ? AND code = ? AND type = ?
              AND verifie = 0 AND expire_at > DATETIME('now')
            LIMIT 1;
            """
            cursor = self.db.executer(requete, (email, code, type_code))
            return cursor.fetchone() is not None
        finally:
            self.db.deconnecter()

    def valider_code(self, email, code, type_code='activation'):
        if not self.db.connecter():
            return False
        try:
            requete = """
            UPDATE code_verification
            SET verifie = 1
            WHERE email = ? AND code = ? AND type = ?;
            """
            self.db.executer(requete, (email, code, type_code))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Validation code : {e}")
            return False
        finally:
            self.db.deconnecter()

    def incrementer_tentative(self, email, type_code='activation'):
        if not self.db.connecter():
            return False
        try:
            # Récupère la tentative du code le plus récent
            requete_check = """
            SELECT tentative FROM code_verification
            WHERE email = ? AND type = ?
            ORDER BY date_envoi DESC
            LIMIT 1;
            """
            cursor = self.db.executer(requete_check, (email, type_code))
            result = cursor.fetchone()

            if result is None:
                return False

            tentative = result[0]

            if tentative >= 4:
                # Expire le code le plus récent
                requete_expire = """
                UPDATE code_verification
                SET tentative = tentative + 1,
                    expire_at = DATETIME('now')
                WHERE email = ? AND type = ?
                AND date_envoi = (
                    SELECT MAX(date_envoi) FROM code_verification
                    WHERE email = ? AND type = ?
                );
                """
                self.db.executer(requete_expire, (email, type_code, email, type_code))
                self.db.commit()
                return 'destroy'
            else:
                # Incrémente simplement la tentative du code le plus récent
                requete_increment = """
                UPDATE code_verification
                SET tentative = tentative + 1
                WHERE email = ? AND type = ?
                AND date_envoi = (
                    SELECT MAX(date_envoi) FROM code_verification
                    WHERE email = ? AND type = ?
                );
                """
                self.db.executer(requete_increment, (email, type_code, email, type_code))
                self.db.commit()
                return True
        except Exception as e:
            print(f"[ERREUR] Incrément tentative : {e}")
            return False
        finally:
            self.db.deconnecter()



    def nettoyer_codes_expirés(self):
        if not self.db.connecter():
            return False
        try:
            requete = """
            DELETE FROM code_verification
            WHERE expire_at <= DATETIME('now') OR verifie = 1;
            """
            self.db.executer(requete)
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Nettoyage codes : {e}")
            return False
        finally:
            self.db.deconnecter()
            