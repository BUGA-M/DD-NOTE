import random
import string

class PasswordGenerateur:
    def __init__(self, length=12):
        if length < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        self.length = length
        self.symbols = "!@#$%&*_+-=?"

    def generate(self):
        # Garantir au moins une minuscule, majuscule, chiffre, symbole
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        symbol = random.choice(self.symbols)

        # Reste des caractères
        remaining_length = self.length - 4
        other_chars = random.choices(
            string.ascii_letters + string.digits + self.symbols,
            k=remaining_length
        )

        # Mélange final
        password_list = list(lowercase + uppercase + digit + symbol + ''.join(other_chars))
        random.shuffle(password_list)
        return ''.join(password_list)

# Exemple d'utilisation
#generator = PasswordGenerateur(length=12)
#password = generator.generate()
#print(password)
