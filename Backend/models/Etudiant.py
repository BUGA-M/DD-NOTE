from Backend.db.connexion import ConnexionDB
from Backend.utils.crypto import Crypto
from datetime import datetime


class EtudiantManager:
    def __init__(self):
        self.db = ConnexionDB()
    
    def email_existe(self, email):
            """Vérifie si un email existe déjà dans la base de données"""
            if not self.db.connecter():
                return False
            try:
                requete = "SELECT 1 FROM etudiant WHERE email = ? LIMIT 1"
                cursor = self.db.executer(requete, (email,))
                return cursor.fetchone() is not None
            finally:
                self.db.deconnecter()

    
    def inscrire_etudiant(self, nom, prenom, email, password, date_naissance,
                          niveau_scolaire, typebac, bac_year, filiere_nom, sexe,
                          adresse="Null", telephone="Null", moyenne_bac=None, classe_id=None, 
                          parent_nom=None, parent_telephone=None, parent_email=None):
        """Inscrit un nouvel étudiant dans la base de données"""
        if not self.db.connecter():
            return False
        try:
            password_chiffre = Crypto.encrypt(password)
            requete = """
                INSERT INTO etudiant (
                    nom, prenom, email, password, date_naissance,
                    niveau_scolaire, typebac, bac_year, filiere_nom, sexe,
                    adresse, telephone, moyenne_bac, classe_id,
                    parent_nom, parent_telephone, parent_email 
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                nom, prenom, email, password_chiffre, date_naissance,
                niveau_scolaire, typebac, bac_year, filiere_nom, sexe,
                adresse, telephone, moyenne_bac, classe_id,
                parent_nom, parent_telephone, parent_email
            )
            self.db.executer(requete, params)
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Inscription étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def get_etudiant_by_id(self, etudiant_id):
        """Récupère un étudiant par son ID"""
        if not self.db.connecter():
            return None
        try:
            requete = "SELECT * FROM etudiant WHERE id = ?"
            cursor = self.db.executer(requete, (etudiant_id,))
            return cursor.fetchone() if cursor else None
        finally:
            self.db.deconnecter()

    def get_etudiant_by_email(self, email):
        """Récupère un étudiant par son email"""
        if not self.db.connecter():
            return None
        try:
            requete = "SELECT * FROM etudiant WHERE email = ?"
            cursor = self.db.executer(requete, (email,))
            return cursor.fetchone() if cursor else None
        finally:
            self.db.deconnecter()

    def get_etudiants_actifs(self):
        """Récupère tous les étudiants avec le statut 'Actif'"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, nom, prenom, email, filiere_nom, niveau_scolaire, statut
                FROM etudiant
                WHERE statut = 'Actif'
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_en_attente_email(self):
        """Récupère tous les étudiants en attente de validation d'email"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, nom, prenom, email, filiere_nom
                FROM etudiant
                WHERE email_valide = 0
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_en_attente_admin(self):
        """Récupère tous les étudiants en attente de validation administrative"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, nom, prenom, email, filiere_nom, bac, moyenne_bac, niveau_scolaire
                FROM etudiant
                WHERE validation_admin = 0
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_par_filiere(self, filiere_nom):
        """Récupère tous les étudiants d'une filière donnée"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, nom, prenom, email, niveau_scolaire, statut
                FROM etudiant
                WHERE filiere_nom = ?
            """
            cursor = self.db.executer(requete, (filiere_nom,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def get_etudiants_par_classe(self, classe_id):
        """Récupère tous les étudiants d'une classe donnée"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT e.id, e.nom, e.prenom, e.email, e.niveau_scolaire, c.nom as nom_classe
                FROM etudiant e
                JOIN classe c ON e.classe_id = c.id
                WHERE e.classe_id = ? AND e.statut = 'Actif'
            """
            cursor = self.db.executer(requete, (classe_id,))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()

    def supprimer_email_non_valide(self, email):
        """
        Supprime un étudiant dont l'email n'est pas validé.
        """
        if not self.db.connecter():
            return False
        try:
            requete = """
                DELETE FROM etudiant
                WHERE email = ? AND email_valide = 0
            """
            self.db.executer(requete, (email.strip().lower(),))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Suppression email non validé : {e}")
            return False
        finally:
            self.db.deconnecter()


    def valider_email(self, email):
        """Valide l'email d'un étudiant en se basant sur son adresse email (unique)"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET email_valide = 1, updated_at = CURRENT_TIMESTAMP
                WHERE email = ?
            """
            self.db.executer(requete, (email.strip().lower(),))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Validation email étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()


    def valider_admin(self, etudiant_id):
        """Valide un étudiant par l'administrateur"""
        if not self.db.connecter():
            return False
        try:
            requete = """
                UPDATE etudiant
                SET validation_admin = 1, statut = 'Actif', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(requete, (etudiant_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Validation admin étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def maj_infos_etudiant(self, etudiant_id, email=None, telephone=None, adresse=None, 
                           parent_nom=None, parent_telephone=None, parent_email=None):
        """Met à jour les informations d'un étudiant"""
        if not self.db.connecter():
            return False
        try:
            # Récupération des informations actuelles
            etudiant = self.get_etudiant_by_id(etudiant_id)
            if not etudiant:
                return False
                
            # Mise à jour des champs uniquement s'ils sont fournis
            new_email = email if email else etudiant['email']
            new_telephone = telephone if telephone else etudiant['telephone']
            new_adresse = adresse if adresse else etudiant['adresse']
            new_parent_nom = parent_nom if parent_nom else etudiant['parent_nom']
            new_parent_telephone = parent_telephone if parent_telephone else etudiant['parent_telephone']
            new_parent_email = parent_email if parent_email else etudiant['parent_email']
            
            requete = """
                UPDATE etudiant
                SET email = ?, telephone = ?, adresse = ?, 
                    parent_nom = ?, parent_telephone = ?, parent_email = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(requete, (new_email, new_telephone, new_adresse, 
                                     new_parent_nom, new_parent_telephone, new_parent_email,
                                     etudiant_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] MAJ infos étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def changer_classe_etudiant(self, etudiant_id, nouvelle_classe_id):
        """Change la classe d'un étudiant"""
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
        """Change le statut d'un étudiant"""
        if not self.db.connecter():
            return False
        try:
            # Vérification que le statut est valide
            statuts_valides = ['Actif', 'Non-Actif', 'Suspendu']
            if nouveau_statut not in statuts_valides:
                return False
                
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

    def changer_password(self, email, nouveau_password):
        """Change le mot de passe d'un étudiant à partir de son email"""
        if not self.db.connecter():
            return False
        try:
            password_chiffre = Crypto.encrypt(nouveau_password)
            requete = """
                UPDATE etudiant
                SET password = ?, updated_at = CURRENT_TIMESTAMP
                WHERE email = ?
            """
            self.db.executer(requete, (password_chiffre, email.strip().lower()))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[ERREUR] Changement de mot de passe étudiant : {e}")
            return False
        finally:
            self.db.deconnecter()

    def supprimer_etudiant(self, etudiant_id):
        """Supprime un étudiant de la base de données"""
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
            
    def rechercher_etudiants(self, terme_recherche):
        """Recherche des étudiants par nom, prénom ou email"""
        if not self.db.connecter():
            return []
        try:
            terme = f"%{terme_recherche}%"
            requete = """
                SELECT id, nom, prenom, email, filiere_nom, niveau_scolaire, statut
                FROM etudiant
                WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?
            """
            cursor = self.db.executer(requete, (terme, terme, terme))
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()
            
    def compter_etudiants_par_filiere(self):
        """Compte le nombre d'étudiants par filière"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT filiere_nom, COUNT(*) as nombre_etudiants
                FROM etudiant
                GROUP BY filiere_nom
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()
            
    def get_tous_etudiants(self):
        """Récupère tous les étudiants de la base de données"""
        if not self.db.connecter():
            return []
        try:
            requete = """
                SELECT id, nom, prenom, email, filiere_nom, niveau_scolaire, statut, validation_admin, email_valide
                FROM etudiant
                ORDER BY nom, prenom
            """
            cursor = self.db.executer(requete)
            return cursor.fetchall() if cursor else []
        finally:
            self.db.deconnecter()