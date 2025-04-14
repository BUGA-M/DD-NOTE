import customtkinter as ctk
from PIL import Image

class FullBackgroundFrame(ctk.CTkFrame):
    def __init__(self, master, image_path, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.image_path = image_path

        # Crée un label pour afficher l’image (initialement vide)
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Mettre à jour le fond à chaque redimensionnement
        self.bind("<Configure>", self._resize_background)

    def _resize_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()

        if width > 0 and height > 0:
            pil_image = Image.open(self.image_path).resize((width, height))
            self.bg_image = ctk.CTkImage(light_image=pil_image, size=(width, height))
            self.bg_label.configure(image=self.bg_image)

# Exemple d’utilisation
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # ou "light"
    app = ctk.CTk()
    app.geometry("800x600")

    bg_frame = FullBackgroundFrame(app, "../DDnote/Custom/pic/bg.jpg")
    bg_frame.pack(fill="both", expand=True)

    # Exemple de widget par-dessus
    label = ctk.CTkLabel(bg_frame, text="Bienvenue !", font=("Arial", 24), text_color="white", bg_color="transparent")
    label.place(relx=0.5, rely=0.1, anchor="center")

    app.mainloop()
