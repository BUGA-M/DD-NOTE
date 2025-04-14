import customtkinter as ctk
from PIL import Image, ImageDraw

class GradientBackgroundFrame(ctk.CTkFrame):
    def __init__(self, master, color1="#1e3a8a", color2="#3b82f6", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.color1 = color1
        self.color2 = color2

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 0 or height <= 0:
            return

        gradient = Image.new("RGB", (width, height), color=0)
        draw = ImageDraw.Draw(gradient)

        r1, g1, b1 = self.winfo_rgb(self.color1)
        r2, g2, b2 = self.winfo_rgb(self.color2)

        r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
        r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256

        for i in range(height):
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        self.gradient_image = ctk.CTkImage(light_image=gradient, size=(width, height))
        self.bg_label.configure(image=self.gradient_image)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("800x600")

    gradient_frame = GradientBackgroundFrame(app, "#0ea5e9", "#1e40af")
    gradient_frame.pack(fill="both", expand=True)

    label = ctk.CTkLabel(gradient_frame, text="Avec un dégradé 😎", text_color="white", font=("Arial", 22))
    label.place(relx=0.5, rely=0.1, anchor="center")

    app.mainloop()
