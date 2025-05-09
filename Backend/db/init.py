import os
import sqlite3
from Backend.config import DB_PATH

class DatabaseInitializer:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

        # Création du répertoire parent si nécessaire
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def database_exists(self):
        """Vérifie l'existence du fichier de base de données."""
        return os.path.exists(self.db_path)

    def connect(self):
        """Établit une connexion à la base de données SQLite."""
        if not self.database_exists():
            raise FileNotFoundError(f"La base de données n'existe pas: {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        return conn, cursor

    def initialize(self):
        """Initialise une nouvelle base de données SQLite (non chiffrée)."""
        if self.database_exists():
            print("[INFO] Base de données déjà existante.")
            return False

        print("[INFO] Initialisation de la base de données...")

        # Supprimer si vide
        if os.path.exists(self.db_path) and os.path.getsize(self.db_path) == 0:
            os.remove(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Création du schéma
        cursor.executescript(self.get_schema_sql())
        conn.commit()
        conn.close()

        print("[✅] Base de données SQLite créée avec succès.")
        return True

    def verify(self):
        """Vérifie que la base est bien lisible."""
        if not self.database_exists():
            print("[❌] Aucune base de données trouvée.")
            return False
        try:
            conn, cursor = self.connect()
            cursor.execute("SELECT name FROM sqlite_master;")
            print("[✅] Accès réussi à la base de données.")
            conn.close()
            return True
        except Exception as e:
            print(f"[❌] Erreur d'accès à la base de données : {e}")
            return False
        
    def get_schema_sql(self):
        return """
        PRAGMA foreign_keys = ON;

        -- Table Administrateurs
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email_recup TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            last_login TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        -- Table Filières
        CREATE TABLE IF NOT EXISTS filiere (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            level TEXT NOT NULL,
            description TEXT,
            parent_id INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES filiere(id) ON DELETE SET NULL ON UPDATE CASCADE
        );

        -- Table Professeurs
        CREATE TABLE IF NOT EXISTS prof (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cin TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            telephone TEXT,
            specialite TEXT,
            status TEXT DEFAULT 'Actif',
            date_embauche TEXT,
            filiere_principale INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (filiere_principale) REFERENCES filiere(id) ON DELETE SET NULL ON UPDATE CASCADE
        );

        -- Table Classes
        CREATE TABLE IF NOT EXISTS classe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            niveau INTEGER,
            annee_academique TEXT,
            filiere_id INTEGER,
            responsable_id INTEGER,
            capacite INTEGER DEFAULT 40,
            salle_principale TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (filiere_id) REFERENCES filiere(id) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY (responsable_id) REFERENCES prof(id) ON DELETE SET NULL ON UPDATE CASCADE,
            UNIQUE (name, annee_academique)
        );

        -- Table Étudiants
        CREATE TABLE IF NOT EXISTS etudiant (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            niveau_scolaire TEXT NOT NULL,
            typebac TEXT NOT NULL,
            bac_year TEXT NOT NULL,
            filiere_nom TEXT NOT NULL,
            sexe TEXT NOT NULL,
            adresse TEXT,
            telephone TEXT,
            moyenne_bac REAL,
            email_valide INTEGER DEFAULT 0, 
            validation_admin INTEGER DEFAULT 0,
            statut TEXT DEFAULT 'Non-Actif',
            classe_id INTEGER,
            parent_nom TEXT,
            parent_telephone TEXT,
            parent_email TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (classe_id) REFERENCES classe(id) ON DELETE SET NULL ON UPDATE CASCADE
        );


        -- Table Modules
        CREATE TABLE IF NOT EXISTS module (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            volume_horaire INTEGER NOT NULL,
            heures_cm INTEGER DEFAULT 0,
            heures_td INTEGER DEFAULT 0,
            heures_tp INTEGER DEFAULT 0,
            nb_examens INTEGER NOT NULL,
            type_efm TEXT NOT NULL,
            coefficient REAL DEFAULT 1.0,
            is_optional INTEGER DEFAULT 0,
            semestre INTEGER,
            filiere_id INTEGER,
            prof_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (filiere_id) REFERENCES filiere(id) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY (prof_id) REFERENCES prof(id) ON DELETE SET NULL ON UPDATE CASCADE
        );

        -- Table Prof_Module
        CREATE TABLE IF NOT EXISTS prof_module (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prof_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            est_responsable INTEGER DEFAULT 0,
            heures_attribuees INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prof_id) REFERENCES prof(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE ON UPDATE CASCADE,
            UNIQUE (prof_id, module_id)
        );

        -- Table Séances
        CREATE TABLE IF NOT EXISTS seance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volume_horaire INTEGER NOT NULL,
            date_heure TEXT NOT NULL,
            heure_fin TEXT,
            salle TEXT,
            type_seance TEXT DEFAULT 'CM',
            statut TEXT DEFAULT 'Planifié',
            validation_admin INTEGER DEFAULT 0,
            validateur_id INTEGER,
            description TEXT,
            prof_id INTEGER,
            module_id INTEGER,
            classe_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prof_id) REFERENCES prof(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (classe_id) REFERENCES classe(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (validateur_id) REFERENCES admin(id) ON DELETE SET NULL ON UPDATE CASCADE
        );

        -- Table Absences
        CREATE TABLE IF NOT EXISTS absence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id INTEGER NOT NULL,
            seance_id INTEGER NOT NULL,
            date_absence TEXT,
            duree_minutes INTEGER DEFAULT 120,
            justification INTEGER DEFAULT 0,
            date_justification TEXT,
            motif TEXT,
            document_path TEXT,
            validee_par INTEGER,
            commentaire TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (etudiant_id) REFERENCES etudiant(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (seance_id) REFERENCES seance(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (validee_par) REFERENCES admin(id) ON DELETE SET NULL ON UPDATE CASCADE
        );

        -- Table Notes
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            semestre INTEGER,
            annee_academique TEXT,
            note1 REAL CHECK (note1 IS NULL OR (note1 >= 0 AND note1 <= 20)),
            note2 REAL CHECK (note2 IS NULL OR (note2 >= 0 AND note2 <= 20)),
            note3 REAL CHECK (note3 IS NULL OR (note3 >= 0 AND note3 <= 20)),
            note4 REAL CHECK (note4 IS NULL OR (note4 >= 0 AND note4 <= 20)),
            note5 REAL CHECK (note5 IS NULL OR (note5 >= 0 AND note5 <= 20)),
            note6 REAL CHECK (note6 IS NULL OR (note6 >= 0 AND note6 <= 20)),
            efm REAL CHECK (efm IS NULL OR (efm >= 0 AND efm <= 20)),
            mg REAL CHECK (mg IS NULL OR (mg >= 0 AND mg <= 20)),
            mention TEXT,
            observations TEXT,
            saisi_par INTEGER,
            validation_admin INTEGER DEFAULT 0,
            validateur_id INTEGER,
            date_validation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (etudiant_id) REFERENCES etudiant(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (saisi_par) REFERENCES prof(id) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY (validateur_id) REFERENCES admin(id) ON DELETE SET NULL ON UPDATE CASCADE,
            UNIQUE (etudiant_id, module_id, annee_academique)
        );
                
        CREATE TABLE IF NOT EXISTS code_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            type TEXT DEFAULT 'activation',
            expire_at DATETIME NOT NULL,
            date_envoi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tentative INTEGER DEFAULT 0,
            verifie INTEGER DEFAULT 0
        );

        """