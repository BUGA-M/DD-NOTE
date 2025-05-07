# Backend/db/connexion.py

import sqlite3
from Backend.config import DB_PATH  

class ConnexionDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connecter(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            return True
        except sqlite3.Error as e:
            print(f"[❌] Erreur de connexion à la base de données : {e}")
            self.deconnecter()
            return False

    def deconnecter(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def executer(self, requete, params=()):
        if not self.cursor:
            print("[❌] Aucune connexion active.")
            return None
        try:
            self.cursor.execute(requete, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"[❌] Erreur lors de l'exécution de la requête : {e}")
            return None
        
    def commit(self):
        if self.connection:
            self.connection.commit()
            
    def executer_many(self, requete, params_list):
        if not self.cursor:
            print("[❌] Aucune connexion active.")
            return None
        try:
            self.cursor.executemany(requete, params_list)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"[❌] Erreur lors de l'exécution multiple : {e}")
            return None

    def fetchall(self, requete, params=()):
        cursor = self.executer(requete, params)
        return cursor.fetchall() if cursor else []

    def fetchone(self, requete, params=()):
        cursor = self.executer(requete, params)
        return cursor.fetchone() if cursor else None
