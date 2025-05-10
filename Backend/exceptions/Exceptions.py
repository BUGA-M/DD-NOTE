class MDPException(Exception):
    """Exception de base pour les erreurs de mot de passe."""
    pass

class MDPVideException(MDPException):
    def __init__(self, message="Le mot de passe est obligatoire."):
        super().__init__(message)

class MDPCourtException(MDPException):
    def __init__(self, message="Le mot de passe doit contenir au moins 8 caractères."):
        super().__init__(message)

class MajException(MDPException):
    def __init__(self, message="Le mot de passe doit contenir au moins une lettre majuscule."):
        super().__init__(message)

class MinException(MDPException):
    def __init__(self, message="Le mot de passe doit contenir au moins une lettre minuscule."):
        super().__init__(message)

class NumberException(MDPException):
    def __init__(self, message="Le mot de passe doit contenir au moins un chiffre."):
        super().__init__(message)

class CaractereException(MDPException):
    def __init__(self, message="Le mot de passe doit contenir au moins un caractère spécial."):
        super().__init__(message)

class MDPdiffException(MDPException):
    def __init__(self, message="Les mots de passe ne correspondent pas."):
        super().__init__(message)
