import customtkinter as ctk
import sqlite3
from tkinter import messagebox, filedialog
from PIL import Image
import os
import shutil
import time

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

DB_NAME = 'crabs.db'
IMAGES_DIR = 'images'

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# FUNCIÓN PARA INICIALIZAR LA BASE DE DATOS
def init_database():
    """Inicializa la base de datos con las tablas necesarias"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Verificar si la tabla species existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='species'")
        if not cursor.fetchone():
            # Crear tabla con todos los campos
            cursor.execute('''
            CREATE TABLE species (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genus TEXT NOT NULL,
                phylum TEXT DEFAULT 'Arthropoda',
                family TEXT DEFAULT 'Galatheidae',
                description TEXT,
                image_url TEXT,
                color TEXT,
                size TEXT,
                location TEXT,
                spines TEXT,
                appendages TEXT,
                carapace_lines INTEGER,
                posterior_spines INTEGER,
                cardiac_spines INTEGER,
                antennular_spine TEXT,
                supraocular_spines TEXT,
                fourth_abdominal_spine INTEGER,
                abdominal_midline_spines INTEGER,
                rostrum_spines INTEGER,
                ocular_peduncle_spines INTEGER,
                gastric_spines TEXT
            )
            ''')
            print("Tabla 'species' creada.")
        else:
            # Verificar si faltan columnas y añadirlas si es necesario
            cursor.execute("PRAGMA table_info(species)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Lista de nuevas columnas para la clave dicotómica
            new_columns = [
                ('carapace_lines', 'INTEGER'),
                ('posterior_spines', 'INTEGER'),
                ('cardiac_spines', 'INTEGER'),
                ('antennular_spine', 'TEXT'),
                ('supraocular_spines', 'TEXT'),
                ('fourth_abdominal_spine', 'INTEGER'),
                ('abdominal_midline_spines', 'INTEGER'),
                ('rostrum_spines', 'INTEGER'),
                ('ocular_peduncle_spines', 'INTEGER'),
                ('gastric_spines', 'TEXT')
            ]
            
            for column_name, column_type in new_columns:
                if column_name not in columns:
                    cursor.execute(f"ALTER TABLE species ADD COLUMN {column_name} {column_type}")
                    print(f"Columna '{column_name}' añadida a la tabla 'species'.")
        
        # Verificar y crear tablas para la clave dicotómica si no existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='key_nodes'")
        if not cursor.fetchone():
            cursor.execute('''
            CREATE TABLE key_nodes (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL
            )
            ''')
            print("Tabla 'key_nodes' creada.")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='key_options'")
        if not cursor.fetchone():
            cursor.execute('''
            CREATE TABLE key_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id INTEGER NOT NULL,
                option_text TEXT NOT NULL,
                next_node_id INTEGER,
                species_id INTEGER,
                FOREIGN KEY (node_id) REFERENCES key_nodes (id),
                FOREIGN KEY (species_id) REFERENCES species (id)
            )
            ''')
            print("Tabla 'key_options' creada.")
        
        conn.commit()
        conn.close()
        print("Base de datos verificada/actualizada.")
        
    except sqlite3.Error as e:
        print(f"Error inicializando la base de datos: {e}")
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

# Inicializar base de datos al inicio
init_database()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Identificador de Especies de Munidopsis")
        self.geometry("1100x700")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Munidopsis App", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_view = ctk.CTkButton(self.sidebar_frame, text="Ver Especies", command=self.show_view_species)
        self.sidebar_button_view.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_register = ctk.CTkButton(self.sidebar_frame, text="Registrar Especie", command=self.show_register_species)
        self.sidebar_button_register.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_identify = ctk.CTkButton(self.sidebar_frame, text="Identificar Especie", command=self.show_identify_species)
        self.sidebar_button_identify.grid(row=3, column=0, padx=20, pady=10)

        # Main content area
        self.main_frame = None
        self.show_view_species()

    def clear_main_frame(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

    def show_view_species(self):
        self.clear_main_frame()
        self.main_frame = ViewSpeciesFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_register_species(self):
        self.clear_main_frame()
        self.main_frame = RegisterSpeciesFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    def show_edit_species(self, species_id):
        self.clear_main_frame()
        self.main_frame = EditSpeciesFrame(self, species_id)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_identify_species(self):
        self.clear_main_frame()
        self.main_frame = IdentifySpeciesFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


def load_local_image(path, size=(150, 150)):
    if not path or not os.path.exists(path):
        return None
    try:
        pil_image = Image.open(path)
        return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None


class ViewSpeciesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="Especies Registradas")
        self.master_app = master
        self.grid_columnconfigure(0, weight=1)
        
        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_search)
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Buscar por nombre o familia...", textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="nsew")
        self.cards_frame.grid_columnconfigure(0, weight=1)
        
        self.load_data()

    def update_search(self, *args):
        self.load_data(self.search_var.get())

    def load_data(self, search_query=""):
        # Clear existing widgets in cards_frame
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            query = "SELECT id, name, genus, phylum, family, description, color, size, location, spines, appendages, image_url FROM species"
            params = ()
            
            if search_query:
                query += " WHERE name LIKE ? OR family LIKE ? OR genus LIKE ?"
                search_term = f"%{search_query}%"
                params = (search_term, search_term, search_term)
            
            cursor.execute(query, params)
            species_list = cursor.fetchall()
            conn.close()

            if not species_list:
                ctk.CTkLabel(self.cards_frame, text="No se encontraron especies.").pack(pady=20)
                return

            for i, species in enumerate(species_list):
                self.create_species_card(i, species)
        except sqlite3.Error as e:
            ctk.CTkLabel(self.cards_frame, text=f"Error: {e}", text_color="red").pack(pady=20)

    def create_species_card(self, index, species):
        s_id, name, genus, phylum, family, description, color, size, location, spines, appendages, image_path = species
        
        card = ctk.CTkFrame(self.cards_frame)
        card.pack(padx=10, pady=10, fill="x")
        card.grid_columnconfigure(1, weight=1)

        # 1. Encabezado (Nombre y Taxonomía)
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkLabel(card, text=f"{phylum} | {family}", text_color="gray").grid(row=1, column=1, padx=10, pady=(0, 5), sticky="w")

        # 2. Cuadrícula de Detalles
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        details = [
            ("Color:", color), ("Tamaño:", size), ("Ubicación:", location),
            ("Espinas:", spines), ("Apéndices:", appendages)
        ]
        
        for i, (label, value) in enumerate(details):
            ctk.CTkLabel(details_frame, text=label, font=ctk.CTkFont(weight="bold")).grid(row=i, column=0, sticky="w", padx=(0, 5))
            ctk.CTkLabel(details_frame, text=value, wraplength=400).grid(row=i, column=1, sticky="w")

        # 3. Descripción
        ctk.CTkLabel(card, text="Descripción:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=1, padx=10, pady=(5,0), sticky="w")
        ctk.CTkLabel(card, text=description, wraplength=500, justify="left").grid(row=4, column=1, padx=10, pady=(0, 10), sticky="w")

        # 4. Imagen
        img = load_local_image(image_path, size=(400, 400))
        if img:
            img_label = ctk.CTkLabel(card, text="", image=img)
            img_label.grid(row=2, column=1, padx=20, pady=20, sticky="e")

        # 5. Botones de Acción
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.grid(row=6, column=1, padx=10, pady=10, sticky="e")
        
        ctk.CTkButton(action_frame, text="Editar", width=80, command=lambda: self.master_app.show_edit_species(s_id)).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Eliminar", width=80, fg_color="red", hover_color="darkred", command=lambda: self.delete_species(s_id, name)).pack(side="left", padx=5)

    def delete_species(self, s_id, name):
        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar a '{name}'?"):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM species WHERE id = ?", (s_id,))
                conn.commit()
                conn.close()
                self.load_data(self.search_var.get())
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))


class RegisterSpeciesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="Registrar Nueva Especie")
        self.master_app = master
        self.grid_columnconfigure(1, weight=1)
        self.entries = {}
        self.selected_image_path = None
        self.setup_form()
    
    def create_form_field(self, row, label_text, field_name, placeholder=""):
        """Crea un campo del formulario con el widget apropiado"""
        ctk.CTkLabel(self, text=label_text + ":").grid(row=row, column=0, padx=20, pady=10, sticky="e")
        
        # Para campos booleanos, usar combobox
        if field_name in ['carapace_lines', 'posterior_spines', 'cardiac_spines',
                         'fourth_abdominal_spine', 'abdominal_midline_spines',
                         'rostrum_spines', 'ocular_peduncle_spines']:
            entry = ctk.CTkComboBox(self, values=["true", "false"])
            if placeholder:
                entry.set(placeholder)  # Usar set() en lugar de placeholder_text
        elif field_name in ['antennular_spine', 'supraocular_spines', 'gastric_spines']:
            # Para campos con opciones específicas
            if field_name == 'antennular_spine':
                values = ["", "externa_larga", "interna_doble"]
            elif field_name == 'supraocular_spines':
                values = ["", "sobrepasa_cornea", "llega_cornea"]
            elif field_name == 'gastric_spines':
                values = ["", "par_grande", "tuberculos", "ninguna"]
            else:
                values = []
            
            entry = ctk.CTkComboBox(self, values=values)
            if placeholder:
                entry.set(placeholder)  # Usar set() en lugar de placeholder_text
        else:
            # Para campos de texto normales, CTkEntry sí acepta placeholder_text
            entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        self.entries[field_name] = entry
    
    def setup_form(self):
        """Configura el formulario con todos los campos"""
        # Campos básicos (existentes)
        basic_fields = [
            ("Nombre científico", "name", ""),
            ("Género", "genus", "Munida o Munidopsis"),
            ("Filum", "phylum", "Arthropoda"),
            ("Familia", "family", "Galatheidae"),
            ("Color", "color", ""),
            ("Tamaño", "size", ""),
            ("Ubicación", "location", ""),
            ("Espinas", "spines", ""),
            ("Apéndices", "appendages", ""),
        ]
        
        for i, (label, key, placeholder) in enumerate(basic_fields):
            self.create_form_field(i, label, key, placeholder)
        
        # Campos para la clave dicotómica (NUEVOS)
        key_fields_start = len(basic_fields)
        key_fields = [
            ("Líneas transversales en caparazón", "carapace_lines", ""),
            ("Espinas en margen posterior", "posterior_spines", ""),
            ("Espinas en región cardíaca", "cardiac_spines", ""),
            ("Espina antenular (comparación)", "antennular_spine", ""),
            ("Espinas supraoculares", "supraocular_spines", ""),
            ("Espina 4to segmento abdominal", "fourth_abdominal_spine", ""),
            ("Espinas línea media abdomen", "abdominal_midline_spines", ""),
            ("Espinas laterales en rostro", "rostrum_spines", ""),
            ("Espinas en pedúnculo ocular", "ocular_peduncle_spines", ""),
            ("Espinas/tubérculos gástricos", "gastric_spines", ""),
        ]
        
        for i, (label, key, placeholder) in enumerate(key_fields):
            row = key_fields_start + i
            self.create_form_field(row, label, key, placeholder)
        
        # Imagen
        row_img = key_fields_start + len(key_fields)
        ctk.CTkLabel(self, text="Imagen:").grid(row=row_img, column=0, padx=20, pady=10, sticky="e")
        self.image_btn = ctk.CTkButton(self, text="Seleccionar Imagen", command=self.select_image)
        self.image_btn.grid(row=row_img, column=1, padx=20, pady=10, sticky="w")
        self.image_label = ctk.CTkLabel(self, text="Ninguna seleccionada")
        self.image_label.grid(row=row_img, column=1, padx=(160, 20), pady=10, sticky="w")
        
        # Descripción
        ctk.CTkLabel(self, text="Descripción:").grid(row=row_img + 1, column=0, padx=20, pady=10, sticky="ne")
        self.textbox_desc = ctk.CTkTextbox(self, height=100)
        self.textbox_desc.grid(row=row_img + 1, column=1, padx=20, pady=10, sticky="ew")
        
        # Botones
        btn_row = row_img + 2
        save_btn = ctk.CTkButton(self, text="Guardar Especie", command=self.save_species)
        save_btn.grid(row=btn_row, column=1, padx=20, pady=20, sticky="e")
        
        cancel_btn = ctk.CTkButton(self, text="Cancelar", fg_color="gray", 
                                  command=self.master_app.show_view_species)
        cancel_btn.grid(row=btn_row, column=0, padx=20, pady=20, sticky="w")
    
    def select_image(self):
        """Selecciona una imagen para la especie"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.image_label.configure(text=os.path.basename(file_path))
    
    def save_species(self):
        """Guarda la nueva especie en la base de datos"""
        print("=== INICIANDO save_species ===")
        
        # Recoger datos básicos
        data = {}
        for key, entry in self.entries.items():
            value = entry.get().strip()
            print(f"Campo: {key} = '{value}'")
            
            # Convertir valores booleanos a enteros (0/1)
            if key in ['carapace_lines', 'posterior_spines', 'cardiac_spines', 
                      'fourth_abdominal_spine', 'abdominal_midline_spines',
                      'rostrum_spines', 'ocular_peduncle_spines']:
                if value.lower() == 'true' or value == '1' or value.lower() == 'sí':
                    data[key] = 1
                elif value.lower() == 'false' or value == '0' or value.lower() == 'no':
                    data[key] = 0
                else:
                    data[key] = None
            else:
                data[key] = value if value else None
        
        description = self.textbox_desc.get("1.0", "end-1c").strip()
        print(f"Descripción: '{description[:50]}...'")
        
        # Validaciones
        if not data.get('name'):
            messagebox.showerror("Error", "El nombre científico es obligatorio.")
            return
        
        if not data.get('genus'):
            messagebox.showerror("Error", "El género es obligatorio.")
            return
        
        # Manejar la imagen
        final_image_path = ""
        if self.selected_image_path:
            print(f"Imagen seleccionada: {self.selected_image_path}")
            try:
                ext = os.path.splitext(self.selected_image_path)[1]
                filename = f"{int(time.time())}_{data['name'].replace(' ', '_')}{ext}"
                dest_path = os.path.join(IMAGES_DIR, filename)
                shutil.copy(self.selected_image_path, dest_path)
                final_image_path = dest_path
                print(f"Imagen guardada en: {final_image_path}")
            except Exception as e:
                print(f"Error copiando imagen: {e}")
                messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")
                return
        else:
            print("No se seleccionó imagen")
        
        try:
            print("Conectando a la base de datos...")
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Preparar los valores para la consulta
            values = (
                data['name'], 
                data['genus'], 
                data.get('phylum', 'Arthropoda'), 
                data.get('family', ''), 
                description, 
                final_image_path,
                data.get('color'), 
                data.get('size'), 
                data.get('location'),
                data.get('spines'), 
                data.get('appendages'),
                data.get('carapace_lines'), 
                data.get('posterior_spines'),
                data.get('cardiac_spines'), 
                data.get('antennular_spine'),
                data.get('supraocular_spines'), 
                data.get('fourth_abdominal_spine'),
                data.get('abdominal_midline_spines'), 
                data.get('rostrum_spines'),
                data.get('ocular_peduncle_spines'), 
                data.get('gastric_spines')
            )
            
            print(f"Valores a insertar: {values}")
            
            # Insertar la especie
            cursor.execute("""
                INSERT INTO species (
                    name, genus, phylum, family, description, image_url,
                    color, size, location, spines, appendages,
                    carapace_lines, posterior_spines, cardiac_spines,
                    antennular_spine, supraocular_spines, fourth_abdominal_spine,
                    abdominal_midline_spines, rostrum_spines, ocular_peduncle_spines,
                    gastric_spines
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            
            conn.commit()
            conn.close()
            
            print("Especie insertada correctamente")
            messagebox.showinfo("Éxito", f"Especie '{data['name']}' registrada correctamente.")
            
            # Limpiar formulario
            self.clear_form()
            
        except sqlite3.Error as e:
            print(f"ERROR SQLite: {e}")
            messagebox.showerror("Error de Base de Datos", str(e))
        except Exception as e:
            print(f"ERROR General: {e}")
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            if hasattr(entry, 'delete'):
                entry.delete(0, "end")
            elif hasattr(entry, 'set'):
                entry.set("")
        self.textbox_desc.delete("1.0", "end")
        self.selected_image_path = None
        self.image_label.configure(text="Ninguna seleccionada")


class EditSpeciesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, species_id):
        super().__init__(master, label_text="Editar Especie")
        self.master_app = master
        self.species_id = species_id
        self.grid_columnconfigure(1, weight=1)
        self.entries = {}
        self.selected_image_path = None
        self.current_db_image_path = ""
        self.load_data()

    def load_data(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Obtener TODOS los campos incluyendo los nuevos
            cursor.execute("""
                SELECT name, genus, phylum, family, description, color, size, location, 
                       spines, appendages, image_url, carapace_lines, posterior_spines, 
                       cardiac_spines, antennular_spine, supraocular_spines, 
                       fourth_abdominal_spine, abdominal_midline_spines, 
                       rostrum_spines, ocular_peduncle_spines, gastric_spines
                FROM species WHERE id = ?
            """, (self.species_id,))
            
            species = cursor.fetchone()
            conn.close()

            if species:
                # Desempaquetar todos los campos
                (name, genus, phylum, family, description, color, size, location, 
                 spines, appendages, image_url, carapace_lines, posterior_spines,
                 cardiac_spines, antennular_spine, supraocular_spines,
                 fourth_abdominal_spine, abdominal_midline_spines,
                 rostrum_spines, ocular_peduncle_spines, gastric_spines) = species
                
                self.current_db_image_path = image_url
                
                # Campos básicos
                basic_fields = [
                    ("Nombre científico", "name", name),
                    ("Género", "genus", genus or "Munida"),
                    ("Filum", "phylum", phylum or "Arthropoda"),
                    ("Familia", "family", family or ""),
                    ("Color", "color", color or ""),
                    ("Tamaño", "size", size or ""),
                    ("Ubicación", "location", location or ""),
                    ("Espinas", "spines", spines or ""),
                    ("Apéndices", "appendages", appendages or ""),
                ]
                
                for i, (label, key, value) in enumerate(basic_fields):
                    self.create_form_entry(i, label, key, value)
                
                # Campos de clave dicotómica
                key_fields = [
                    ("Líneas transversales en caparazón", "carapace_lines", carapace_lines),
                    ("Espinas en margen posterior", "posterior_spines", posterior_spines),
                    ("Espinas en región cardíaca", "cardiac_spines", cardiac_spines),
                    ("Espina antenular (comparación)", "antennular_spine", antennular_spine or ""),
                    ("Espinas supraoculares", "supraocular_spines", supraocular_spines or ""),
                    ("Espina 4to segmento abdominal", "fourth_abdominal_spine", fourth_abdominal_spine),
                    ("Espinas línea media abdomen", "abdominal_midline_spines", abdominal_midline_spines),
                    ("Espinas laterales en rostro", "rostrum_spines", rostrum_spines),
                    ("Espinas en pedúnculo ocular", "ocular_peduncle_spines", ocular_peduncle_spines),
                    ("Espinas/tubérculos gástricos", "gastric_spines", gastric_spines or ""),
                ]
                
                start_row = len(basic_fields)
                for i, (label, key, value) in enumerate(key_fields):
                    self.create_form_entry(start_row + i, label, key, value)
                
                # Imagen
                row_img = start_row + len(key_fields)
                ctk.CTkLabel(self, text="Imagen:").grid(row=row_img, column=0, padx=20, pady=10, sticky="e")
                self.image_btn = ctk.CTkButton(self, text="Cambiar Imagen", command=self.select_image)
                self.image_btn.grid(row=row_img, column=1, padx=20, pady=10, sticky="w")
                
                img_text = os.path.basename(image_url) if image_url else "Ninguna"
                self.image_label = ctk.CTkLabel(self, text=img_text)
                self.image_label.grid(row=row_img, column=1, padx=(160, 20), pady=10, sticky="w")
                
                # Descripción
                ctk.CTkLabel(self, text="Descripción:").grid(row=row_img + 1, column=0, padx=20, pady=10, sticky="ne")
                self.textbox_desc = ctk.CTkTextbox(self, height=100)
                self.textbox_desc.grid(row=row_img + 1, column=1, padx=20, pady=10, sticky="ew")
                self.textbox_desc.insert("1.0", description or "")
                
                # Botones
                btn_row = row_img + 2
                save_btn = ctk.CTkButton(self, text="Actualizar Especie", command=self.update_species)
                save_btn.grid(row=btn_row, column=1, padx=20, pady=20, sticky="e")
                
                cancel_btn = ctk.CTkButton(self, text="Cancelar", fg_color="gray", 
                                          command=self.master_app.show_view_species)
                cancel_btn.grid(row=btn_row, column=0, padx=20, pady=20, sticky="w")

        except sqlite3.Error as e:
            ctk.CTkLabel(self, text=f"Error: {e}", text_color="red").pack()

    def create_form_entry(self, row, label_text, field_name, value=""):
        """Crea un campo del formulario con el valor adecuado"""
        ctk.CTkLabel(self, text=label_text + ":").grid(row=row, column=0, padx=20, pady=10, sticky="e")
        
        # Para campos booleanos, usar combobox
        if field_name in ['carapace_lines', 'posterior_spines', 'cardiac_spines',
                         'fourth_abdominal_spine', 'abdominal_midline_spines',
                         'rostrum_spines', 'ocular_peduncle_spines']:
            entry = ctk.CTkComboBox(self, values=["true", "false"])
            if value is not None:
                entry.set("true" if value else "false")
            else:
                entry.set("")  # Valor vacío por defecto
        elif field_name in ['antennular_spine', 'supraocular_spines', 'gastric_spines']:
            # Para campos con opciones específicas
            if field_name == 'antennular_spine':
                values = ["", "externa_larga", "interna_doble"]
            elif field_name == 'supraocular_spines':
                values = ["", "sobrepasa_cornea", "llega_cornea"]
            elif field_name == 'gastric_spines':
                values = ["", "par_grande", "tuberculos", "ninguna"]
            else:
                values = []
            
            entry = ctk.CTkComboBox(self, values=values)
            entry.set(value or "")
        else:
            # Para campos de texto normales
            entry = ctk.CTkEntry(self)
            if value:
                entry.insert(0, str(value))
        
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        self.entries[field_name] = entry

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.image_label.configure(text=os.path.basename(file_path))

    def update_species(self):
        """Actualiza la especie con todos los campos"""
        # Recoger datos de todos los campos
        data = {}
        for key, entry in self.entries.items():
            value = entry.get().strip()
            
            # Convertir valores booleanos
            if key in ['carapace_lines', 'posterior_spines', 'cardiac_spines',
                      'fourth_abdominal_spine', 'abdominal_midline_spines',
                      'rostrum_spines', 'ocular_peduncle_spines']:
                data[key] = 1 if value.lower() == 'true' else 0
            else:
                data[key] = value if value else None
        
        description = self.textbox_desc.get("1.0", "end-1c").strip()
        
        # Validaciones
        if not data.get('name'):
            messagebox.showerror("Error", "El nombre científico es obligatorio.")
            return
        
        if not data.get('genus'):
            messagebox.showerror("Error", "El género es obligatorio.")
            return
        
        # Manejar la imagen
        final_image_path = self.current_db_image_path
        if self.selected_image_path:
            try:
                ext = os.path.splitext(self.selected_image_path)[1]
                filename = f"{int(time.time())}_{data['name'].replace(' ', '_')}{ext}"
                dest_path = os.path.join(IMAGES_DIR, filename)
                shutil.copy(self.selected_image_path, dest_path)
                final_image_path = dest_path
                
                # Eliminar imagen anterior si existe y no es la predeterminada
                if (self.current_db_image_path and 
                    os.path.exists(self.current_db_image_path) and
                    not self.current_db_image_path.endswith("default_crab.jpg")):
                    try:
                        os.remove(self.current_db_image_path)
                    except:
                        pass
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")
                return
        
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Actualizar TODOS los campos
            cursor.execute("""
                UPDATE species SET 
                    name=?, genus=?, phylum=?, family=?, description=?, 
                    image_url=?, color=?, size=?, location=?, spines=?, 
                    appendages=?, carapace_lines=?, posterior_spines=?,
                    cardiac_spines=?, antennular_spine=?, supraocular_spines=?,
                    fourth_abdominal_spine=?, abdominal_midline_spines=?,
                    rostrum_spines=?, ocular_peduncle_spines=?, gastric_spines=?
                WHERE id=?
            """, (
                data['name'], data['genus'], data.get('phylum'), 
                data.get('family'), description, final_image_path,
                data.get('color'), data.get('size'), data.get('location'),
                data.get('spines'), data.get('appendages'),
                data.get('carapace_lines'), data.get('posterior_spines'),
                data.get('cardiac_spines'), data.get('antennular_spine'),
                data.get('supraocular_spines'), data.get('fourth_abdominal_spine'),
                data.get('abdominal_midline_spines'), data.get('rostrum_spines'),
                data.get('ocular_peduncle_spines'), data.get('gastric_spines'),
                self.species_id
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "Especie actualizada correctamente.")
            self.master_app.show_view_species()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", str(e))


class IdentifySpeciesFrame(ctk.CTkFrame):
    """
    Pantalla de identificación de especies mediante clave dicotómica (13 nodos)
    con sistema de puntuación por rasgos morfológicos en tiempo real.
    """

    # Mapeo: node_id → (columna_en_species, valor_si_la_respuesta_es_'SÍ', valor_si_es_'NO')
    NODE_TRAIT_MAP = {
        1:  ("carapace_lines",          1, 0),
        2:  ("posterior_spines",        1, 0),
        6:  ("ocular_peduncle_spines",  1, 0),
        7:  ("ocular_peduncle_spines",  1, 0),
        11: ("cardiac_spines",          1, 0),
        13: ("carapace_lines",          0, 1),   # nodo 13: liso = carapace_lines=0
    }

    def __init__(self, master):
        super().__init__(master)
        self.master_app = master

        # Estado
        self.history = []          # [(node_id, question_text, answer_text, is_yes)]
        self.species_scores = {}   # {species_id: int}
        self.all_species = {}      # {species_id: dict con todos los campos}

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Encabezado ──────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Identificador de Especies  —  Clave Dicotómica + Puntuación",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(20, 8))

        # ── Marco central ────────────────────────────────────────────────────────
        mid = ctk.CTkFrame(self)
        mid.grid(row=1, column=0, sticky="nsew", padx=20, pady=8)
        mid.grid_columnconfigure(0, weight=3)
        mid.grid_columnconfigure(1, weight=1)
        mid.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        self.left = ctk.CTkFrame(mid)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        self.left.grid_columnconfigure(0, weight=1)
        self.left.grid_rowconfigure(1, weight=1)

        self.q_label = ctk.CTkLabel(
            self.left, text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=560, justify="left",
        )
        self.q_label.grid(row=0, column=0, padx=18, pady=18, sticky="w")

        self.opts = ctk.CTkScrollableFrame(self.left)
        self.opts.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.opts.grid_columnconfigure(0, weight=1)

        # Panel derecho
        right = ctk.CTkFrame(mid)
        right.grid(row=0, column=1, sticky="nsew", pady=8)

        ctk.CTkLabel(
            right, text="Estado",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(14, 4))

        self.step_lbl = ctk.CTkLabel(right, text="Paso 1", font=ctk.CTkFont(size=12))
        self.step_lbl.pack()

        # Géneros
        gf = ctk.CTkFrame(right)
        gf.pack(fill="x", padx=8, pady=6)
        ctk.CTkLabel(gf, text="Géneros:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=6, pady=(4, 0))
        ctk.CTkLabel(gf, text="• Munida (4 spp.)\n• Munidopsis (6 spp.)", justify="left",
                     font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=(0, 6))

        # Top candidatos
        cf = ctk.CTkFrame(right)
        cf.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(cf, text="Top candidatos:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=6, pady=(4, 0))
        self.cand_lbl = ctk.CTkLabel(cf, text="—", justify="left",
                                     font=ctk.CTkFont(size=11), wraplength=155)
        self.cand_lbl.pack(anchor="w", padx=10, pady=(0, 6))

        # Historial
        hf = ctk.CTkFrame(right)
        hf.pack(fill="both", expand=True, padx=8, pady=6)
        ctk.CTkLabel(hf, text="Historial:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", pady=(4, 2))
        self.hist_box = ctk.CTkTextbox(hf, font=ctk.CTkFont(size=10))
        self.hist_box.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        self.hist_box.configure(state="disabled")

        # ── Controles ────────────────────────────────────────────────────────────
        ctrl = ctk.CTkFrame(self, fg_color="transparent")
        ctrl.grid(row=2, column=0, pady=(0, 14))

        self.back_btn = ctk.CTkButton(ctrl, text="← Anterior", width=130,
                                      state="disabled", command=self.go_back)
        self.back_btn.pack(side="left", padx=6)

        ctk.CTkButton(ctrl, text="↺ Reiniciar", width=130,
                      fg_color="#b03030", hover_color="#802020",
                      command=self.reset).pack(side="left", padx=6)

        # Cargar datos y arrancar
        self._load_species()
        self.load_node(1)

    # ── Carga de datos ───────────────────────────────────────────────────────────

    def _load_species(self):
        """Carga todas las especies de la DB para el sistema de puntuación."""
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("""
                SELECT id, name, genus, phylum, family, description, image_url,
                       color, size, location, spines, appendages,
                       carapace_lines, posterior_spines, cardiac_spines,
                       antennular_spine, supraocular_spines,
                       fourth_abdominal_spine, abdominal_midline_spines,
                       rostrum_spines, ocular_peduncle_spines, gastric_spines
                FROM species ORDER BY genus, name
            """)
            cols = [d[0] for d in c.description]
            for row in c.fetchall():
                d = dict(zip(cols, row))
                self.all_species[d["id"]] = d
                self.species_scores[d["id"]] = 0
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error DB", str(e))

    # ── Navegación de la clave ────────────────────────────────────────────────────

    def load_node(self, node_id):
        """Carga pregunta y opciones de un nodo."""
        self.current_node_id = node_id
        for w in self.opts.winfo_children():
            w.destroy()
        self.back_btn.configure(state="normal" if self.history else "disabled")

        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()

            c.execute("SELECT question FROM key_nodes WHERE id=?", (node_id,))
            row = c.fetchone()
            if not row:
                messagebox.showerror("Error", f"Nodo {node_id} no encontrado en la clave.")
                conn.close()
                return
            question = row[0]
            self.q_label.configure(text=question)

            c.execute("""
                SELECT id, option_text, next_node_id, species_id
                FROM key_options WHERE node_id=? ORDER BY id
            """, (node_id,))
            options = c.fetchall()
            conn.close()

            for opt_id, text, next_nd, sp_id in options:
                btn = ctk.CTkButton(
                    self.opts, text=text, height=52,
                    font=ctk.CTkFont(size=13),
                    fg_color="transparent", border_width=2,
                    corner_radius=10, anchor="w",
                    command=lambda n=next_nd, s=sp_id, t=text, q=question:
                        self.handle_option(node_id, q, t, n, s),
                )
                btn.pack(fill="x", padx=6, pady=5)

            self.step_lbl.configure(text=f"Paso {len(self.history) + 1}")
            self._refresh_candidates()

        except sqlite3.Error as e:
            messagebox.showerror("Error BD", str(e))

    def handle_option(self, node_id, question, answer_text, next_node, species_id):
        """Procesa la selección del usuario y actualiza puntuación."""
        is_yes = answer_text.upper().startswith("SÍ") or answer_text.upper().startswith("SI")
        self.history.append((node_id, question, answer_text, is_yes))
        self._apply_scoring(node_id, is_yes)
        self._update_history()
        self._refresh_candidates()

        if species_id:
            self.show_result(species_id)
        elif next_node:
            self.load_node(next_node)
        else:
            messagebox.showerror("Error", "La clave dicotómica está incompleta en este punto.")

    def go_back(self):
        """Deshace el último paso."""
        if not self.history:
            return
        node_id, question, answer_text, was_yes = self.history.pop()
        # Revertir puntuación
        self._apply_scoring(node_id, was_yes, revert=True)
        self._update_history()
        self._refresh_candidates()
        # Volver al nodo anterior
        if self.history:
            self.load_node(self.history[-1][0])
        else:
            self.load_node(1)

    def reset(self, ask=True):
        """Reinicia la identificación."""
        if ask and not messagebox.askyesno("Reiniciar", "¿Reiniciar desde el principio?"):
            return
        self.history.clear()
        for sid in self.species_scores:
            self.species_scores[sid] = 0
        self.hist_box.configure(state="normal")
        self.hist_box.delete("1.0", "end")
        self.hist_box.configure(state="disabled")
        self.cand_lbl.configure(text="—")

        # Restaurar panel izquierdo si fue reemplazado por el resultado
        for w in self.left.winfo_children():
            w.destroy()
        self.q_label = ctk.CTkLabel(
            self.left, text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=560, justify="left",
        )
        self.q_label.grid(row=0, column=0, padx=18, pady=18, sticky="w")
        self.opts = ctk.CTkScrollableFrame(self.left)
        self.opts.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.opts.grid_columnconfigure(0, weight=1)
        self.load_node(1)

    # ── Motor de puntuación ───────────────────────────────────────────────────────

    def _apply_scoring(self, node_id, is_yes, revert=False):
        """Aplica (o revierte) la puntuación basada en una respuesta."""
        trait_info = self.NODE_TRAIT_MAP.get(node_id)
        if not trait_info:
            return
        col, yes_val, no_val = trait_info
        expected = yes_val if is_yes else no_val
        delta = -1 if revert else 1

        for sid, sp in self.all_species.items():
            sp_val = sp.get(col)
            if sp_val is not None and int(sp_val) == int(expected):
                self.species_scores[sid] += delta

    def _get_ranked_species(self):
        """Devuelve lista de (score, species_id, species_name) ordenada desc."""
        ranked = [
            (score, sid, self.all_species[sid]["name"])
            for sid, score in self.species_scores.items()
            if sid in self.all_species
        ]
        ranked.sort(key=lambda x: -x[0])
        return ranked

    def _confidence(self, score):
        """Calcula el % de confianza a partir del score y el número de pasos."""
        steps = len(self.history)
        if steps == 0:
            return 0
        max_possible = steps
        raw = score / max_possible if max_possible else 0
        return min(100.0, max(0.0, raw * 100))

    # ── Actualización de UI ──────────────────────────────────────────────────────

    def _refresh_candidates(self):
        ranked = self._get_ranked_species()
        if not ranked or len(self.history) == 0:
            self.cand_lbl.configure(text="—")
            return
        lines = []
        for i, (sc, sid, sname) in enumerate(ranked[:3]):
            pct = self._confidence(sc)
            short = sname.split()[1] if len(sname.split()) > 1 else sname
            bar = "█" * int(pct / 25) + "░" * (4 - int(pct / 25))
            lines.append(f"{i+1}. {short}\n   {bar} {pct:.0f}%")
        self.cand_lbl.configure(text="\n\n".join(lines))

    def _update_history(self):
        self.hist_box.configure(state="normal")
        self.hist_box.delete("1.0", "end")
        for i, (nid, question, answer, _) in enumerate(self.history):
            short_q = question[:38] + "…" if len(question) > 40 else question
            self.hist_box.insert("end", f"{i+1}. {short_q}\n   → {answer}\n\n")
        self.hist_box.configure(state="disabled")
        self.hist_box.see("end")

    # ── Pantalla de resultado ─────────────────────────────────────────────────────

    def show_result(self, species_id):
        """Muestra el resultado final con detalles completos y confianza."""
        for w in self.left.winfo_children():
            w.destroy()
        self.left.grid_rowconfigure(0, weight=1)

        sp = self.all_species.get(species_id)
        if not sp:
            messagebox.showerror("Error", f"Especie ID {species_id} no encontrada.")
            return

        score = self.species_scores.get(species_id, 0)
        confidence = self._confidence(score)
        # La clave dicotómica garantiza al menos 80% cuando lleva directamente
        confidence = max(confidence, 80.0) if self.history else 95.0

        # Scroll frame para el resultado
        res = ctk.CTkScrollableFrame(self.left)
        res.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        res.grid_columnconfigure(0, weight=1)

        # Banner
        col_banner = "#27ae60" if confidence >= 80 else "#e67e22" if confidence >= 55 else "#c0392b"
        banner = ctk.CTkFrame(res, fg_color=col_banner, corner_radius=10)
        banner.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 6))
        ctk.CTkLabel(
            banner, text="✔  ESPECIE IDENTIFICADA",
            font=ctk.CTkFont(size=17, weight="bold"), text_color="white",
        ).pack(pady=(10, 2))
        ctk.CTkLabel(
            banner, text=f"Confianza de la clave: {confidence:.0f}%",
            font=ctk.CTkFont(size=13), text_color="white",
        ).pack(pady=(0, 10))

        # Nombre científico
        nf = ctk.CTkFrame(res, corner_radius=10)
        nf.grid(row=1, column=0, sticky="ew", padx=8, pady=5)
        ctk.CTkLabel(
            nf, text=sp["name"],
            font=ctk.CTkFont(size=19, weight="bold", slant="italic"),
        ).pack(pady=(12, 2))
        ctk.CTkLabel(
            nf, text=f"Género: {sp['genus']}   •   Familia: {sp['family']}",
            font=ctk.CTkFont(size=13),
        ).pack(pady=(0, 12))

        # Imagen
        img_path = sp.get("image_url", "")
        if img_path and os.path.exists(img_path):
            img_frame = ctk.CTkFrame(res, corner_radius=10)
            img_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=5)
            img = load_local_image(img_path, size=(260, 195))
            if img:
                lbl = ctk.CTkLabel(img_frame, image=img, text="")
                lbl.image = img
                lbl.pack(pady=10)

        # Datos morfológicos
        mf = ctk.CTkFrame(res, corner_radius=10)
        mf.grid(row=3, column=0, sticky="ew", padx=8, pady=5)
        ctk.CTkLabel(mf, text="Características morfológicas:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(10, 4))
        for label, key in [("Color", "color"), ("Tamaño", "size"), ("Localización", "location"),
                            ("Espinas", "spines"), ("Apéndices", "appendages")]:
            val = sp.get(key)
            if val:
                row_f = ctk.CTkFrame(mf, fg_color="transparent")
                row_f.pack(fill="x", padx=12, pady=2)
                ctk.CTkLabel(row_f, text=f"{label}:", font=ctk.CTkFont(size=12, weight="bold"),
                             width=90, anchor="e").pack(side="left")
                ctk.CTkLabel(row_f, text=val, font=ctk.CTkFont(size=12),
                             wraplength=390, justify="left").pack(side="left", padx=(6, 0))
        ctk.CTkFrame(mf, height=6, fg_color="transparent").pack()

        # Descripción
        desc = sp.get("description")
        if desc:
            df = ctk.CTkFrame(res, corner_radius=10)
            df.grid(row=4, column=0, sticky="ew", padx=8, pady=5)
            ctk.CTkLabel(df, text="Descripción general:",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(10, 4))
            ctk.CTkLabel(df, text=desc, wraplength=490, justify="left",
                         font=ctk.CTkFont(size=12)).pack(padx=12, pady=(0, 12))

        # Top alternativas según scoring
        ranked = self._get_ranked_species()
        alts = [(sc, sid, nm) for sc, sid, nm in ranked if sid != species_id and sc > 0]
        if alts:
            af = ctk.CTkFrame(res, corner_radius=10)
            af.grid(row=5, column=0, sticky="ew", padx=8, pady=5)
            ctk.CTkLabel(af, text="Especies alternativas con rasgos similares:",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(10, 4))
            for sc, sid, nm in alts[:3]:
                pct = self._confidence(sc)
                ctk.CTkLabel(af, text=f"  • {nm}  ({pct:.0f}%)",
                             font=ctk.CTkFont(size=12), justify="left").pack(anchor="w", padx=16)
            ctk.CTkFrame(af, height=6, fg_color="transparent").pack()

        # Botones
        bf = ctk.CTkFrame(res, fg_color="transparent")
        bf.grid(row=6, column=0, pady=12)
        ctk.CTkButton(bf, text="↺ Identificar otra",
                      command=lambda: self.reset(ask=False)).pack(side="left", padx=6)
        ctk.CTkButton(bf, text="📋 Ver tabla de especies",
                      fg_color="gray40", hover_color="gray30",
                      command=lambda: self.master_app.show_view_species()).pack(side="left", padx=6)

        self._update_history()
        self._refresh_candidates()


if __name__ == "__main__":
    app = App()
    app.mainloop()
