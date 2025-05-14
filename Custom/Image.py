import customtkinter as ctk
import os
import hashlib
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw,ImageOps

class CreateImage(ctk.CTkImage):
    def __init__(self, path: str = None, lightPath: str = None, darkPath: str = None, width: int = 100, height: int = 100):
        self.defaultImage = Path("../DD-NOTE/Custom/pic/default-IMG.png").resolve()

        self.path = path if path else self.defaultImage
        self.lightPath = lightPath if lightPath else self.path
        self.darkPath = darkPath if darkPath else self.path

        for imgPath in [self.path, self.lightPath, self.darkPath]:
            if imgPath and not os.path.exists(imgPath):
                raise FileNotFoundError(f"Le fichier image '{imgPath}' n'existe pas.")

        super().__init__(
            light_image=Image.open(self.lightPath),
            dark_image=Image.open(self.darkPath),
            size=(width, height)
        )

        self.ico_image = None
        try:
            img = Image.open(self.path)
            img = img.resize((32, 32))
            self.ico_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Warning: Impossible de créer l'icône de fenêtre: {e}")
            
            
    def resize(self, width, height):
        light = Image.open(self.lightPath).resize((width, height), Image.LANCZOS)
        dark = Image.open(self.darkPath).resize((width, height), Image.LANCZOS)
        self.configure(light_image=light, dark_image=dark, size=(width, height))


    def as_ctk(self):
        return self

    def as_icon(self):
        return self.ico_image
    
    def select_image(self):
        """
        Permet de sélectionner une image depuis votre ordinateur.
        
        Returns:
            str: Chemin du fichier image sélectionné ou None si aucun fichier n'est sélectionné
        """
        # Ouvrir le sélecteur de fichier en utilisant customtkinter
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp")
        ]
        
        selected_file = ctk.filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=filetypes
        )
        
        if not selected_file:
            print("Aucun fichier sélectionné")
            return None
            
        return selected_file
            
    def make_circular(self, image_path, width=100, height=100):
        """
        Convertit une image en forme circulaire avec des bords lissés.
        Vérifie si l'image circulaire existe déjà avant de la recréer.
        
        """
        try:
            # Vérifier si le fichier source existe
            if not os.path.isfile(image_path):
                print(f"[❌] Fichier introuvable : {image_path}")
                return None
                
            # Créer un dossier temporaire dans le même répertoire que l'image source
            temp_dir = os.path.join(os.path.dirname(image_path), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Déterminer la taille carrée à partir des dimensions demandées
            size = min(width, height)
            
            # Générer un identifiant unique basé sur le chemin et la taille
            # pour permettre de retrouver l'image si elle existe déjà
            file_hash = hashlib.md5(f"{image_path}_{size}".encode()).hexdigest()[:8]
            unique_name = f"circular_{file_hash}.png"
            temp_path = os.path.join(temp_dir, unique_name)
            
            # Vérifier si l'image circulaire existe déjà
            if os.path.isfile(temp_path):
                # Vérifier si l'image source a été modifiée depuis la dernière conversion
                source_mtime = os.path.getmtime(image_path)
                temp_mtime = os.path.getmtime(temp_path)
                
                if temp_mtime >= source_mtime:
                    print(f"[✓] Image circulaire existante utilisée : {temp_path}")
                    return CreateImage(
                        path=temp_path,
                        lightPath=temp_path,
                        darkPath=temp_path,
                        width=size,
                        height=size
                    )
            
            # Ouvrir et traiter l'image
            with Image.open(image_path).convert("RGBA") as original_img:
                # Centrer et recadrer l'image pour qu'elle soit carrée
                square_img = ImageOps.fit(original_img, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))
                
                # Créer un masque circulaire avec bords lissés
                mask = Image.new('L', (size, size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, size, size), fill=255)
                
                # Appliquer le masque à l'image
                circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                circular_img.paste(square_img, (0, 0), mask=mask)
                
                # Sauvegarder l'image avec une qualité optimisée
                circular_img.save(temp_path, optimize=True)
            
            print(f"[✅] Image circulaire créée : {temp_path}")
            return CreateImage(
                path=temp_path,
                lightPath=temp_path,
                darkPath=temp_path,
                width=size,
                height=size
            )
        
        except Exception as e:
            print(f"[❌] Erreur lors de la création de l'image circulaire : {e}")
            import traceback
            traceback.print_exc()  # Afficher la pile d'appels pour faciliter le débogage
            return None
