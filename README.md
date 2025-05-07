# 🎓 DD-NOTE-OFPPT – Gestion des Notes avec Vérification OTP

Un système graphique complet et sécurisé développé en **Python** pour gérer les études dans les établissements ISTA, avec réinitialisation de mot de passe via **OTP** et une interface moderne basée sur **`customtkinter`**.

---

![Banner](./assets/banner.png)

![GitHub stars](https://img.shields.io/github/stars/BUGA-M/DD-NOTE?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/BUGA-M/DD-NOTE?style=flat-square)
![GitHub license](https://img.shields.io/github/license/BUGA-M/DD-NOTE?style=flat-square)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=flat-square)

---

## ✨ Fonctionnalités Clés

- 🔐 **Vérification par Email (OTP)** – Envoi d'un code sécurisé via `smtplib`
- ⏱️ **Minuteur de validité (5 min)** – Code expiré automatiquement
- ⚡ **Vérification instantanée** – Retour immédiat sur l'état du code
- 🔒 **Réinitialisation sécurisée du mot de passe**
- 🖼️ **Interface moderne et responsive** – Thème clair/sombre, polices customisées
- 🧩 **Structure modulaire claire** – Séparation Frontend / Backend / UI

---

## 🖥️ Aperçu

![Aperçu Acceuil](./Custom/pic/acc.png)
![Aperçu OTP](./Custom/pic/otp.png)

---

## 🚀 Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/BUGA-M/DD-NOTE.git
cd DD-NOTE
```

### 2️⃣ Créer un fichier .env
Créez un fichier `.env` à la racine du projet avec les variables suivantes :
```
EMAIL_SENDER=youremail@gmail.com
EMAIL_PASSWORD=your_email_password
```
> ✅ Utilisez un mot de passe d'application pour Gmail si 2FA est activée.

### 3️⃣ Créer le fichier Backend/config.py
```python
# Backend/config.py
import os

# Clé de chiffrement Fernet (à générer avec Fernet.generate_key())
FERNET_KEY = b"your_fernet_key_here"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'dd_note.db')
```

> 🔐 Pour générer une clé Fernet :
> ```python
> from cryptography.fernet import Fernet
> print(Fernet.generate_key())
> ```

### 4️⃣ Lancer le programme
```bash
python main.py
```

---

## 📁 Structure du projet

```
DD-NOTE/
├── .env                    # Informations d'identification email (non versionné)
├── .gitignore              # Fichiers à ignorer par git
├── dd_note.db              # Base de données SQLite
├── fernet_key.py           # Script pour générer la clé Fernet
├── main.py                 # Point d'entrée de l'application
├── pyproject.toml          # Configuration du projet Python (optionnel)
├── README.md               # Documentation du projet
├── requirements.txt        # Dépendances Python
├── test.csv                # Exemple de fichier CSV (utilitaire ?)
├── test.py                 # Script de test
├── Test/                   # Dossier de tests unitaires
│   └── test-fernet.py
├── Backend/                # Backend (OTP, sécurité, base de données, logique)
│   ├── __init__.py
│   ├── config.py           # Clé Fernet + chemin vers la DB
│   ├── data/
│   ├── db/
│   ├── exceptions/
│   ├── models/
│   ├── services/
│   └── utils/
├── Custom/                 # Composants graphiques personnalisés
│   ├── __init__.py
│   ├── db_fonts/
│   ├── Pic/
│   ├── Position/
│   ├── Button.py
│   ├── ChangeFrame.py
│   ├── ComboBox.py
│   ├── DataBase.py
│   ├── Entry.py
│   ├── Font.py
│   ├── Frame.py
│   ├── Image.py
│   ├── Label.py
│   ├── OptionMenu.py
│   ├── Popup.py
│   ├── secondWindow.py
│   ├── theme_colors.json
│   ├── Theme_controls.py
│   └── Theme_current.json
├── Frontend/               # Interface utilisateur (écrans, frames)
│   ├── __init__.py
│   ├── fonts_installed/
│   ├── Change_Password.py
│   ├── connexion.py
│   ├── CreatAccount.py
│   ├── ForgetPassword.py
│   ├── OTP_Email.py
│   ├── OTP.py
│   └── Saisie.py
└── venv/                   # Environnement virtuel (à ignorer dans .gitignore)

```

---

## 🛡️ Sécurité

- ✅ Chiffrement des mots de passe via Fernet (cryptography)
- 🔁 Code OTP temporaire avec durée limitée
- 🚫 Accès protégé aux fonctions critiques

---

## 📋 Prérequis

- flake8
- bandit
- black
- customtkinter
- pillow
- tk
- dotenv
- cryptography
- pysqlcipher3

---

## 📦 Dépendances

Installez les dépendances nécessaires :

```bash
pip install -r 'requirements.txt'
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push sur la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

---

## 📧 Contact

BUGA-M - [@github](https://github.com/BUGA-M)

Lien du projet : [https://github.com/BUGA-M/DD-NOTE](https://github.com/BUGA-M/DD-NOTE)