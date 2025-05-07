from Backend.db.connexion import ConnexionDB
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.db = ConnexionDB()
        if not self.db.connecter():
            raise Exception("Connexion à la base de données échouée")

    def ajouter_note_initiale(self, etudiant_id, module_id, semestre, annee_academique, note_valeur, saisi_par, observations=None):
        """Ajoute une ligne de note si elle n'existe pas déjà (avec note1)."""
        requete = """
            INSERT INTO note (
                etudiant_id, module_id, semestre, annee_academique, note1, saisi_par, observations
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (etudiant_id, module_id, annee_academique) 
            DO UPDATE SET 
                note1 = excluded.note1,
                observations = COALESCE(excluded.observations, note.observations),
                updated_at = CURRENT_TIMESTAMP
        """
        self.db.executer(requete, (etudiant_id, module_id, semestre, annee_academique, note_valeur, saisi_par, observations))
        return "Note initiale ajoutée ou mise à jour"

    def ajouter_note_continue(self, etudiant_id, module_id, annee_academique, nouvelle_note, numero_note=None):
        """
        Ajoute la note continue spécifiée ou la prochaine disponible (note2 à note6).
        Si numero_note est fourni (2-6), met à jour cette note spécifique.
        Sinon, trouve la première colonne vide et y ajoute la note.
        """
        if numero_note and (numero_note < 1 or numero_note > 6):
            return "Numéro de note invalide. Doit être entre 1 et 6."
            
        requete = """
            SELECT id, note1, note2, note3, note4, note5, note6
            FROM note
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        result = self.db.executer(requete, (etudiant_id, module_id, annee_academique))
        row = result.fetchone()

        if not row:
            return "Aucune ligne trouvée. Veuillez d'abord ajouter une note initiale."

        # Si un numéro de note spécifique est fourni
        if numero_note:
            update = f"""
                UPDATE note 
                SET note{numero_note} = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(update, (nouvelle_note, row["id"]))
            return f"Note{numero_note} mise à jour avec succès"
        
        # Sinon, trouve la première colonne disponible
        for i in range(2, 7):
            if row[f"note{i}"] is None:
                update = f"""
                    UPDATE note 
                    SET note{i} = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                self.db.executer(update, (nouvelle_note, row["id"]))
                return f"Note ajoutée dans note{i}"

        return "Toutes les notes continues sont déjà remplies."

    def ajouter_efm(self, etudiant_id, module_id, annee_academique, efm):
        """Ajoute ou met à jour la note EFM."""
        update = """
            UPDATE note
            SET efm = ?, updated_at = CURRENT_TIMESTAMP
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        rows_affected = self.db.executer(update, (efm, etudiant_id, module_id, annee_academique)).rowcount
        
        if rows_affected == 0:
            return "Aucune ligne trouvée pour mettre à jour l'EFM."
        
        # Calculer automatiquement la moyenne après ajout de l'EFM
        self.calculer_moyenne_et_mention(etudiant_id, module_id, annee_academique)
        return "EFM enregistré et moyenne recalculée."

    def calculer_moyenne_et_mention(self, etudiant_id, module_id, annee_academique):
        """Calcule la moyenne générale (50% CC + 50% EFM) et attribue la mention."""
        requete = """
            SELECT id, note1, note2, note3, note4, note5, note6, efm
            FROM note
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        result = self.db.executer(requete, (etudiant_id, module_id, annee_academique))
        row = result.fetchone()

        if not row:
            return "Aucune note trouvée."

        # Collecter toutes les notes continues non nulles
        notes_continues = [row[f'note{i}'] for i in range(1, 7) if row[f'note{i}'] is not None]

        if not notes_continues:
            return "Pas de notes continues disponibles."

        moyenne_cc = sum(notes_continues) / len(notes_continues)
        efm = row["efm"]

        if efm is None:
            # Mise à jour de la note sans calculer MG (pas d'EFM)
            update = """
                UPDATE note
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            self.db.executer(update, (row["id"],))
            return "EFM manquant pour le calcul final."

        # Calcul de la moyenne générale avec pondération
        mg = round((moyenne_cc * 0.5) + (efm * 0.5), 2)

        mention = (
            "Très Bien" if mg >= 16 else
            "Bien" if mg >= 14 else
            "Assez Bien" if mg >= 12 else
            "Passable" if mg >= 10 else
            "Insuffisant"
        )

        update = """
            UPDATE note
            SET mg = ?, mention = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.db.executer(update, (mg, mention, row["id"]))
        return f"Moyenne: {mg} | Mention: {mention}"

    def valider_note(self, etudiant_id, module_id, annee_academique, validateur_id):
        """Valide une note par l'admin."""
        # Vérifier si la moyenne a été calculée avant validation
        requete = """
            SELECT mg FROM note
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        result = self.db.executer(requete, (etudiant_id, module_id, annee_academique))
        row = result.fetchone()
        
        if not row or row["mg"] is None:
            return "La note ne peut pas être validée. Moyenne non calculée."
        
        update = """
            UPDATE note
            SET validation_admin = 1,
                validateur_id = ?,
                date_validation = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        self.db.executer(update, (validateur_id, etudiant_id, module_id, annee_academique))
        return "Note validée avec succès"

    def annuler_validation(self, etudiant_id, module_id, annee_academique):
        """Annule la validation d'une note."""
        update = """
            UPDATE note
            SET validation_admin = 0,
                validateur_id = NULL,
                date_validation = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        self.db.executer(update, (etudiant_id, module_id, annee_academique))
        return "Validation annulée"

    def get_notes_etudiant(self, etudiant_id, annee_academique=None):
        """Récupère toutes les notes d'un étudiant, avec filtre optionnel par année académique."""
        requete = """
            SELECT n.*, m.nom as module_nom, m.code as module_code, e.nom as etudiant_nom, e.prenom as etudiant_prenom
            FROM note n
            JOIN module m ON n.module_id = m.id
            JOIN etudiant e ON n.etudiant_id = e.id
            WHERE n.etudiant_id=?
        """
        params = [etudiant_id]
        
        if annee_academique:
            requete += " AND n.annee_academique=?"
            params.append(annee_academique)
        
        result = self.db.executer(requete, tuple(params))
        return result.fetchall()

    def get_notes_par_module(self, module_id, annee_academique=None, semestre=None):
        """Récupère toutes les notes pour un module spécifique."""
        requete = """
            SELECT n.*, e.nom as etudiant_nom, e.prenom as etudiant_prenom
            FROM note n
            JOIN etudiant e ON n.etudiant_id = e.id
            WHERE n.module_id=?
        """
        params = [module_id]
        
        if annee_academique:
            requete += " AND n.annee_academique=?"
            params.append(annee_academique)
            
        if semestre:
            requete += " AND n.semestre=?"
            params.append(semestre)
            
        result = self.db.executer(requete, tuple(params))
        return result.fetchall()

    def ajouter_observations(self, etudiant_id, module_id, annee_academique, observations):
        """Ajoute ou met à jour des observations pour une note."""
        update = """
            UPDATE note
            SET observations = ?, updated_at = CURRENT_TIMESTAMP
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        self.db.executer(update, (observations, etudiant_id, module_id, annee_academique))
        return "Observations mises à jour"

    def get_statistiques_module(self, module_id, annee_academique):
        """Calcule les statistiques pour un module (moyenne, max, min, taux de réussite)."""
        requete = """
            SELECT 
                COUNT(*) as total_etudiants,
                AVG(mg) as moyenne_generale,
                MAX(mg) as note_max,
                MIN(mg) as note_min,
                SUM(CASE WHEN mg >= 10 THEN 1 ELSE 0 END) as nb_reussite,
                SUM(CASE WHEN mention = 'Très Bien' THEN 1 ELSE 0 END) as nb_tres_bien,
                SUM(CASE WHEN mention = 'Bien' THEN 1 ELSE 0 END) as nb_bien,
                SUM(CASE WHEN mention = 'Assez Bien' THEN 1 ELSE 0 END) as nb_assez_bien,
                SUM(CASE WHEN mention = 'Passable' THEN 1 ELSE 0 END) as nb_passable,
                SUM(CASE WHEN mention = 'Insuffisant' THEN 1 ELSE 0 END) as nb_insuffisant
            FROM note
            WHERE module_id=? AND annee_academique=? AND mg IS NOT NULL
        """
        result = self.db.executer(requete, (module_id, annee_academique))
        stats = result.fetchone()
        
        if stats and stats["total_etudiants"] > 0:
            taux_reussite = (stats["nb_reussite"] / stats["total_etudiants"]) * 100
            stats["taux_reussite"] = round(taux_reussite, 2)
        
        return stats

    def supprimer_note(self, etudiant_id, module_id, annee_academique):
        """Supprime une ligne de note."""
        # Vérifier si la note est validée avant suppression
        requete = """
            SELECT validation_admin FROM note
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        result = self.db.executer(requete, (etudiant_id, module_id, annee_academique))
        row = result.fetchone()
        
        if row and row["validation_admin"] == 1:
            return "Impossible de supprimer une note validée par l'administration"
            
        delete = """
            DELETE FROM note
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        self.db.executer(delete, (etudiant_id, module_id, annee_academique))
        return "Note supprimée avec succès"

    def get_historique_notes(self, etudiant_id, semestre=None):
        """Récupère l'historique des notes d'un étudiant avec des informations détaillées."""
        requete = """
            SELECT 
                n.*,
                m.nom as module_nom,
                m.code as module_code,
                p.nom as professeur_nom,
                p.prenom as professeur_prenom,
                a.nom as admin_nom,
                a.prenom as admin_prenom
            FROM note n
            JOIN module m ON n.module_id = m.id
            LEFT JOIN prof p ON n.saisi_par = p.id
            LEFT JOIN admin a ON n.validateur_id = a.id
            WHERE n.etudiant_id=?
        """
        params = [etudiant_id]
        
        if semestre:
            requete += " AND n.semestre=?"
            params.append(semestre)
            
        requete += " ORDER BY n.annee_academique DESC, n.semestre ASC, m.nom ASC"
        
        result = self.db.executer(requete, tuple(params))
        return result.fetchall()

    def reset_note_specifique(self, etudiant_id, module_id, annee_academique, numero_note):
        """Réinitialise une note spécifique (de 1 à 6 ou efm)."""
        if numero_note not in [1, 2, 3, 4, 5, 6, 'efm']:
            return "Numéro de note invalide. Doit être entre 1 et 6 ou 'efm'."
            
        colonne = 'efm' if numero_note == 'efm' else f'note{numero_note}'
        
        update = f"""
            UPDATE note
            SET {colonne} = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE etudiant_id=? AND module_id=? AND annee_academique=?
        """
        self.db.executer(update, (etudiant_id, module_id, annee_academique))
        
        # Recalculer la moyenne si nécessaire
        if numero_note == 'efm' or numero_note in [1, 2, 3, 4, 5, 6]:
            self.calculer_moyenne_et_mention(etudiant_id, module_id, annee_academique)
            
        return f"Note {colonne} réinitialisée et moyenne recalculée"