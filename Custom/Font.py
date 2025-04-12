import os
import shutil
import platform
import subprocess

class FontInstaller:
    fonts_installed = {}
    font_install_path = os.path.join(os.path.dirname(__file__), "fonts_installed")

    @staticmethod
    def set_install_path(path: str):
        FontInstaller.font_install_path = path
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def installerFont(name: str, file_path: str, size: int = 16):
        """
        Installe une police personnalisée pour CustomTkinter (nom + taille).
        Copie la police si besoin, met à jour le cache (Linux), puis retourne (nom, taille).
        """
        if name in FontInstaller.fonts_installed:
            return FontInstaller.fonts_installed[name]

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")

        os.makedirs(FontInstaller.font_install_path, exist_ok=True)
        dest_path = os.path.join(FontInstaller.font_install_path, os.path.basename(file_path))

        if not os.path.exists(dest_path):
            shutil.copy(file_path, dest_path)
            print(f"📁 Police copiée dans : {dest_path}")

            if platform.system() == "Linux":
                subprocess.run(["fc-cache", "-f", "-v"])
        else:
            print(f"✅ Police déjà présente : {dest_path}")

        FontInstaller.fonts_installed[name] = (name, size)
        return (name, size)

    @staticmethod
    def get_font(name: str, size: int = 12):
        """Retourne le tuple (nom, taille) pour CustomTkinter"""
        return FontInstaller.fonts_installed.get(name, (name, size))
