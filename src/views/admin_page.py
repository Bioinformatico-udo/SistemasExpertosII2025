
""" ************************** 
    ***     ADMIN PAGE     *** 
    ************************** """
# Este archivo contiene la clase AdminPage que se encarga de gestionar la interfaz de administración.

# --- Importaciones ---
import customtkinter as ctk
import os
from src.models.database import db
from tkinter import messagebox, filedialog

# --- Clase principal ---
class AdminPage(ctk.CTkFrame):
    def __init__(self, master, on_logout, controller):
        super().__init__(master, fg_color="transparent")
        self.on_logout = on_logout
        self.controller = controller
        
        self.setup_ui()

    # --- Función de configuración de la interfaz ---
    def setup_ui(self):
        # Barra superior redondeada
        self.header = ctk.CTkFrame(self, height=70, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        self.logo_label = ctk.CTkLabel(self.header, text="SEITH Admin", font=("Segoe UI", 20, "bold"), text_color="cyan")
        self.logo_label.pack(side="left", padx=20, pady=15)
        
        self.btn_logout = ctk.CTkButton(
            self.header, 
            text="Cerrar Sesión", 
            width=100, 
            height=35, 
            corner_radius=15, 
            fg_color="#CC0000", # Rojo suave
            hover_color="#990000",
            command=self.on_logout
        )
        self.btn_logout.pack(side="right", padx=20, pady=15)

        # Contenido principal con Tabview para separar Especies y Usuarios
        self.tabs = ctk.CTkTabview(self, corner_radius=20)
        self.tabs.pack(fill="both", expand=True, padx=30, pady=(10, 30))
        
        self.tab_species = self.tabs.add("Gestión de Especies")
        self.tab_users = self.tabs.add("Gestión de Usuarios")

        # --- SECCIÓN ESPECIES ---
        self.title_species = ctk.CTkLabel(self.tab_species, text="Base de Conocimientos Taxonómicos", font=("Segoe UI", 20, "bold"))
        self.title_species.pack(pady=10)

        self.actions_frame = ctk.CTkFrame(self.tab_species, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=40)
        
        self.btn_add = ctk.CTkButton(
            self.actions_frame, text="+ Añadir Nueva Especie", corner_radius=20, height=40,
            fg_color="#006666", command=self.show_add_dialog
        )
        self.btn_add.pack(side="left", padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_species, corner_radius=15)
        self.scroll_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # --- SECCIÓN USUARIOS ---
        self.title_users = ctk.CTkLabel(self.tab_users, text="Usuarios Registrados en el Sistema", font=("Segoe UI", 20, "bold"))
        self.title_users.pack(pady=10)

        self.users_scroll = ctk.CTkScrollableFrame(self.tab_users, corner_radius=15)
        self.users_scroll.pack(fill="both", expand=True, padx=40, pady=20)

        self.load_species()
        self.load_users()

    def load_users(self):
        # Limpiar lista anterior
        for widget in self.users_scroll.winfo_children():
            widget.destroy()
            
        users_data = self.controller.get_all_users()
        for u in users_data:
            u_id, u_name, u_role = u
            item = ctk.CTkFrame(self.users_scroll, corner_radius=10, fg_color="#1a1a1a")
            item.pack(fill="x", pady=5, padx=5)
            
            icon = "👤" if u_role == "user" else "🔑"
            color = "white" if u_role == "user" else "cyan"
            
            ctk.CTkLabel(item, text=f"{icon} {u_name}", font=("Segoe UI", 14, "bold"), text_color=color).pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(item, text=f"Rol: {u_role.upper()}", font=("Segoe UI", 11)).pack(side="left", padx=20)
            
            if u_name != "admin": # No se puede borrar al superadmin
                btn_del_user = ctk.CTkButton(
                    item, text="Eliminar", width=80, corner_radius=10, fg_color="#440000",
                    command=lambda name=u_name: self.confirm_delete_user(name)
                )
                btn_del_user.pack(side="right", padx=10)

    def confirm_delete_user(self, username):
        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al usuario '{username}'?"):
            if self.controller.delete_user(username):
                messagebox.showinfo("Éxito", "Usuario eliminado")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    # --- Función de carga de especies ---
    def load_species(self):
        # Limpiar lista anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        species_data = self.controller.get_all_species()
        for s in species_data:
            species_id = s[0]
            item = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#1a1a1a")
            item.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(item, text=f"🧬 {s[1]} {s[2]}", font=("Segoe UI", 16, "bold"), text_color="cyan").pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(item, text=f"Nombre común: {s[3]}", font=("Segoe UI", 12)).pack(side="left", padx=20)
            
            # Botones de Editar y Eliminar
            btn_delete = ctk.CTkButton(
                item, 
                text="Eliminar", 
                width=80, 
                corner_radius=10, 
                fg_color="#330000",
                command=lambda id=species_id: self.confirm_delete(id)
            )
            btn_delete.pack(side="right", padx=10)

            btn_edit = ctk.CTkButton(
                item, 
                text="Editar", 
                width=80, 
                corner_radius=10, 
                fg_color="#004d4d",
                command=lambda data=s: self.show_edit_dialog(data)
            )
            btn_edit.pack(side="right", padx=5)

    # --- Función de confirmación de eliminación ---
    def confirm_delete(self, species_id):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar esta especie?"):
            if self.controller.delete_species(species_id):
                messagebox.showinfo("Éxito", "Especie eliminada")
                self.load_species()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    # --- Función de mostrar diálogo de adición ---
    def show_add_dialog(self):
        self.open_species_dialog()

    # --- Función de mostrar diálogo de edición ---
    def show_edit_dialog(self, data):
        self.open_species_dialog(data)

    # --- Función de mostrar diálogo de adición o edición ---
    def open_species_dialog(self, data=None):
        title = "Editar Especie" if data else "Añadir Nueva Especie"
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("600x750")
        dialog.grab_set()
        
        # Centrar
        x = self.winfo_x() + 250
        y = self.winfo_y() + 50
        dialog.geometry(f"+{x}+{y}")

        self.temp_image_path = None # Para guardar la ruta seleccionada

        ctk.CTkLabel(dialog, text=title, font=("Segoe UI", 20, "bold"), text_color="cyan").pack(pady=20)

        # Contenedor de Formulario
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)

        genus = ctk.CTkEntry(form_frame, placeholder_text="Género (Ej: Emerita)", width=400, height=40, corner_radius=10)
        genus.pack(pady=5)
        if data: genus.insert(0, data[1])

        species = ctk.CTkEntry(form_frame, placeholder_text="Especie (Ej: analoga)", width=400, height=40, corner_radius=10)
        species.pack(pady=5)
        if data: species.insert(0, data[2])

        common_name = ctk.CTkEntry(form_frame, placeholder_text="Nombre Común", width=400, height=40, corner_radius=10)
        common_name.pack(pady=5)
        if data: common_name.insert(0, data[3])

        # --- SECCIÓN DE RASGOS (NUEVO: SELECCIÓN DE DATOS) ---
        ctk.CTkLabel(form_frame, text="Rasgos Taxonómicos (Selección):", font=("Segoe UI", 12, "bold"), text_color="cyan").pack(pady=(10, 5))
        
        traits_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        traits_frame.pack(fill="x")

        # Selectores de rasgos
        ctk.CTkLabel(traits_frame, text="Forma Caparazón:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=2)
        shape_opt = ctk.CTkOptionMenu(traits_frame, values=["ovalado", "subcilindrico", "redondeado"], width=180)
        shape_opt.grid(row=0, column=1, pady=2, padx=10)

        ctk.CTkLabel(traits_frame, text="Superficie:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=2)
        surf_opt = ctk.CTkOptionMenu(traits_frame, values=["liso", "rugoso", "estriado", "granulado"], width=180)
        surf_opt.grid(row=1, column=1, pady=2, padx=10)

        ctk.CTkLabel(traits_frame, text="Dáctilo (Pata):", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=2)
        dact_opt = ctk.CTkOptionMenu(traits_frame, values=["recto", "falcado", "ovalado dactilo"], width=180)
        dact_opt.grid(row=2, column=1, pady=2, padx=10)

        ctk.CTkLabel(traits_frame, text="Talla Máxima:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=2)
        size_opt = ctk.CTkOptionMenu(traits_frame, values=["pequeño", "mediano", "grande"], width=180)
        size_opt.grid(row=3, column=1, pady=2, padx=10)

        # Cargar datos si es edición
        if data and data[5]:
            current_f = data[5].lower()
            if "subcilindrico" in current_f: shape_opt.set("subcilindrico")
            elif "redondeado" in current_f: shape_opt.set("redondeado")
            else: shape_opt.set("ovalado")

            if "rugoso" in current_f: surf_opt.set("rugoso")
            elif "estriado" in current_f: surf_opt.set("estriado")
            elif "granulado" in current_f: surf_opt.set("granulado")
            else: surf_opt.set("liso")

            if "falcado" in current_f: dact_opt.set("falcado")
            elif "ovalado dactilo" in current_f: dact_opt.set("ovalado dactilo")
            else: dact_opt.set("recto")

            if "grande" in current_f: size_opt.set("grande")
            elif "mediano" in current_f: size_opt.set("mediano")
            else: size_opt.set("pequeño")

        # --- SECCIÓN DE IMAGEN ---
        ctk.CTkLabel(form_frame, text="Imagen de REFERENCIA (Visual):", font=("Segoe UI", 12)).pack(pady=(15, 0))
        
        img_preview = ctk.CTkLabel(form_frame, text="Sin Imagen", width=120, height=120, corner_radius=10, fg_color="#1a1a1a")
        img_preview.pack(pady=5)

        if data and data[6]:
            img_path = os.path.join(os.getcwd(), data[6])
            if os.path.exists(img_path):
                from PIL import Image
                img_ref = ctk.CTkImage(Image.open(img_path), size=(110, 110))
                img_preview.configure(image=img_ref, text="")

        def pick_ref_image():
            path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
            if path:
                self.temp_image_path = path
                from PIL import Image
                img_ref = ctk.CTkImage(Image.open(path), size=(110, 110))
                img_preview.configure(image=img_ref, text="")

        ctk.CTkButton(form_frame, text="Cargar Imagen de Referencia", width=180, height=30, corner_radius=15, command=pick_ref_image).pack(pady=5)

        def save_action():
            if not genus.get() or not species.get():
                messagebox.showwarning("Error", "Género y Especie obligatorios")
                return

            # Combinar rasgos en un string estructurado
            combined_features = f"{shape_opt.get()}, {surf_opt.get()}, {dact_opt.get()}, {size_opt.get()}"

            if data: # UPDATE
                success = self.controller.update_species(
                    data[0], genus.get(), species.get(), common_name.get(), "", 
                    combined_features, self.temp_image_path
                )
            else: # CREATE
                success = self.controller.add_species(
                    genus.get(), species.get(), common_name.get(), "", 
                    combined_features, self.temp_image_path
                )

            if success:
                messagebox.showinfo("Éxito", "Especie guardada correctamente")
                self.load_species()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Error al guardar en base de datos")

        ctk.CTkButton(dialog, text="GUARDAR CAMBIOS", corner_radius=20, height=45, fg_color="#008080", command=save_action).pack(pady=20)
        ctk.CTkButton(dialog, text="SALIR", corner_radius=22, height=35, fg_color="transparent", border_width=1, command=dialog.destroy).pack(pady=(0, 20))
