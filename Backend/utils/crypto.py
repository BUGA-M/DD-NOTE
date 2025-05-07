# backend/utils/crypto.py

from cryptography.fernet import Fernet
from Backend.config import FERNET_KEY

class Crypto:
    """Classe utilitaire pour chiffrer et déchiffrer les données avec Fernet."""

    _fernet = Fernet(FERNET_KEY)

    @classmethod
    def encrypt(cls, data: str) -> str:
        """Chiffre une chaîne de caractères (réversible)."""
        return cls._fernet.encrypt(data.encode()).decode()

    @classmethod
    def decrypt(cls, token: str) -> str:
        """Déchiffre une chaîne chiffrée par Fernet."""
        return cls._fernet.decrypt(token.encode()).decode()
