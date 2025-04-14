import customtkinter as ctk
from Custom import CreatLabel ,CreatFrame,FontInstaller,CreatButton,Places
from PIL import Image
import os

class ConnexionFrame(CreatFrame):
    def __init__(self, master):
        super().__init__(
            master,
            600,
            400,
            "#1e293b",
            "#1e293b", 
            20   
        )
        
        title_font = FontInstaller.get_font("Titan One")
        subtitle_font = FontInstaller.get_font("Poppins")
    
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
            subtitle_font[0],
            "#94a3b8",  
            "transparent"
        )
        self.labelSubtitle.LabelPlace(0.5, 0.25)

        self.ligne = CreatFrame(self, 350, 2, fg_color="#475569")
        self.ligne.FramePlace(rely=0.30)
        
        self.roles = ["Admin", "Etudiant", "Prof"]
        self.role_icons = ["🔐", "📚", "👨"]  
        self.buttons = []
        
        for i, (role, icon) in enumerate(zip(self.roles, self.role_icons)):
            btn = CreatButton(
                self, 
                f"{icon}  {role}", 
                270, 
                270,  
                fg_color='#334155',  
                text_font=subtitle_font[0],
                hover_color='#0ea5e9',  
                font_size=18,
                border_width=1,
                border_color='#64748b', 
                corner_radius=10 
            )
            self.buttons.append(btn)
        
        self.footer = CreatLabel(
            self,
            Text="© 2025 DDnote - Système de gestion des notes",
            Font_size=subtitle_font[1] -10,
            text_font=subtitle_font[0],
            text_color="#64748b",
            bg_color="transparent"
        )
        self.footer.LabelPlace(relx=0.5, rely=0.95, anchor="center")
        
        self.bind("<Configure>", self.update_layout)
        
    def update_layout(self, event=None):
        window_width = self.winfo_width()

        if window_width < 900: 
            
            for i, btn in enumerate(self.buttons):
                
                btn.configure(height=80)
                btn.buttonPlace(relx=0.5, rely=0.45 + (i * 0.15), anchor="center")
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

    def show(self):
        self.FrameGride(padx=100, pady=10) 



    