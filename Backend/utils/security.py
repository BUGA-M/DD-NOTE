# backend/utils/security.py

from Backend.utils.crypto import Crypto
import hashlib
import hmac
import os

class Security:
    """Classe pour sécuriser les données sensibles."""

    @staticmethod
    def encrypt_data(data: str) -> str:
        """Chiffre les données sensibles (réversibles)."""
        return encrypt(data)

    @staticmethod
    def decrypt_data(data: str) -> str:
        """Déchiffre les données sensibles."""
        return decrypt(data)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hache un mot de passe (non réversible)."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Vérifie qu'un mot de passe correspond à un hash donné."""
        return hmac.compare_digest(Security.hash_password(password), hashed)

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Génère un token aléatoire sécurisé (ex : pour reset password)."""
        return os.urandom(length).hex()
