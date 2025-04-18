import customtkinter as ctk
from Custom import CreatLabel ,CreatFrame,FontInstaller,CreatButton,Places,CreateImage,ThemeControls,ThemeManager,ThemeColors,ChangeFrame
from PIL import Image
import os
from pathlib import Path


current_dir = os.path.dirname(os.path.abspath(__file__))
font_dir = os.path.join(current_dir, "fonts_installed")
FontInstaller.set_install_path(font_dir)


class ConnexionFrame(CreatFrame):
    def __init__(self, master,FrameSinscrire):
        super().__init__(
            master,
            600,
            400,
            "transparent",
            "transparent", 
            20   
        )
        self.FrameSinscrire=FrameSinscrire
        title_font = FontInstaller.get_font("Titan One")
        subtitle_font = FontInstaller.get_font("Poppins")
        type_font = FontInstaller.get_font("Orbitron")
        
        #self.bg_image = CreateImage("../DDnote/Custom/pic/bg8.jpg", width=self.winfo_width(), height=self.winfo_height())
        #self.bg_label = CreatLabel(
        #    self,
        #    text="",
        #    image=self.bg_image,
        #    bg_color="transparent"
        #)
        #self.bg_label.LabelPlace(relwidth=1, relheight=1)

        self.labelTitle = CreatLabel(
            self,
            "DDnote",
            title_font[1],
            title_font[0],
            "#3b82f6",  
            "transparent"
        )
        self.labelTitle.LabelPlace(0.5, 0.10,)
        
        self.labelSubtitle = CreatLabel(
            self,
            "Sélectionnez votre profil pour continuer",
            subtitle_font[1] - 5,
            type_font[0],
            "red",  
            "transparent"
        )
        self.labelSubtitle.LabelPlace(0.5, 0.22)

        self.ligne = CreatFrame(self, 385, 2, fg_color="#475569")
        self.ligne.FramePlace(rely=0.25)
        
        self.roles = ["Admin", "Stagaire", "Formateur"]

        self.path_images = [Path("./Custom/pic/admin.png").resolve(),
                            Path("./Custom/pic/Stagaire.png").resolve(),
                            Path("./Custom/pic/Formateur.png").resolve()
                            ] 
        self.buttons = []
        
        for i, (role, pic, sinc) in enumerate(zip(self.roles, self.path_images,self.FrameSinscrire)):
            btn = CreatButton(
                self, 
                f"{role}", 
                270, 
                270,  
                fg_color='#334155',  
                text_font=type_font[0],
                hover_color='#0ea5e9',  
                font_size=18,
                border_width=1,
                border_color='#64748b', 
                corner_radius=10 ,
                image=CreateImage(str(pic)),
                compound="top",
                command=lambda frame=sinc : master.manager.show_frame(frame)
            )
            self.buttons.append(btn)
        
        self.footer = CreatLabel(
            self,
            text="© 2025 DDnote - Système de gestion des notes",
            font_size=subtitle_font[1] - 10,
            text_font=subtitle_font[0],
            text_color="#64748b",
            bg_color="transparent"
        )

        self.footer.LabelPlace(relx=0.5, rely=0.98, anchor="center")
        
        self.bind("<Configure>", self.update_layout)
        
        self.apply_theme_colors()

    def update_layout(self, event=None):
        #new_width = self.winfo_width()
        #new_height = self.winfo_height()
        
        #self.bg_image.configure(size=(new_width, new_height))
         
        window_width = self.winfo_width()

        if window_width < 900: 
            
            for i, btn in enumerate(self.buttons):
                
                btn.configure(height=150)
                btn.buttonPlace(relx=0.5, rely=0.38 + (i * 0.23), anchor="center")
        else: 
            max_button_area_width = 900 
            
            for btn in self.buttons:
                btn.configure(height=270)
            
            button_width = 270  
            buttons_count = len(self.buttons)
            
            spacing = min(0.35, (max_button_area_width / window_width) / buttons_count)
            
            start_offset = 0.5 - ((buttons_count - 1) * spacing / 2)
            
            for i, btn in enumerate(self.buttons):
                relx = start_offset + i * spacing
                btn.buttonPlace(relx=relx, rely=0.6, anchor="center")
        self.showPack()
    def apply_theme_colors(self):
        theme_name = ThemeManager.load_theme_preference()["color_theme"]
        theme_data = ThemeColors.load_colors(theme_name)

        self.labelTitle.configure(text_color=theme_data["title"])
        self.labelSubtitle.configure(text_color=theme_data["subtitle"])
        self.footer.configure(text_color=theme_data["footer"])

        for btn in self.buttons:
            btn.configure(
                fg_color=theme_data["button"],
                hover_color=theme_data["button_hover"],
                border_color=theme_data["border"]
            )

    def showGrid(self):
        self.FrameGride(padx=0, pady=0) 
    def showPack(self):
        self.FramePack()

    