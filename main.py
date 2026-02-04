""" ************************** 
    ***       MAIN.PY      *** 
    ************************** """

# --- Importaciones ---
import customtkinter as ctk
from src.views.login_page import LoginPage
from src.views.admin_page import AdminPage
from src.views.user_page import UserPage
from src.controllers.main_controller import MainController

# --- Clase Principal ---
class SeithApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de apariencia
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("SEITH - Sistema Experto")
        self.geometry("1100x800")
        
        # Centrar ventana en pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (1100 // 2)
        y = (screen_height // 2) - (800 // 2)
        self.geometry(f"1100x800+{x}+{y}")

        self.controller = MainController()
        self.user_role = None
        
        # Contenedor principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_login()

    # --- Métodos de acceso---
    def show_login(self):
        self.clear_container()
        login_view = LoginPage(self.container, self.show_admin, self.show_user, self.controller)
        login_view.pack(fill="both", expand=True)

    def show_admin(self):
        self.clear_container()
        admin_view = AdminPage(self.container, self.show_login, self.controller)
        admin_view.pack(fill="both", expand=True)

    def show_user(self):
        self.clear_container()
        user_view = UserPage(self.container, self.show_login, self.controller)
        user_view.pack(fill="both", expand=True)

    # --- Métodos de utilidad ---
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

# --- Ejecución ---
if __name__ == "__main__":
    app = SeithApp()
    app.mainloop()
