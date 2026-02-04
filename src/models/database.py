""" ************************** 
    ***     DATABASE.PY    *** 
    ************************** """
# Este archivo contiene la clase Database que se encarga de gestionar la base de datos.

# Importaciones
import sqlite3
import os
import hashlib

# Clase Database
class Database:
    def __init__(self, db_name="seith_data.db"):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.init_db()

    def _hash_password(self, password):
        """Genera un hash SHA-256 para la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de Usuarios y Roles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
                    api_key TEXT -- Columna para persistir la llave de la IA
                )
            ''')
            
            # Intentar añadir la columna api_key si no existe (para migraciones)
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN api_key TEXT")
            except:
                pass

            # Tabla de Especies (Base de Conocimientos)
            # Aquí guardaremos los rasgos taxonómicos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS species (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    genus TEXT NOT NULL,
                    species TEXT NOT NULL,
                    common_name TEXT,
                    description TEXT,
                    key_features TEXT, -- JSON o texto con rasgos
                    image_path TEXT
                )
            ''')

            # Insertar administrador por defecto si no existe
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", self._hash_password("admin123"), "admin")
                )
            
            # Insertar usuario por defecto si no existe
            cursor.execute("SELECT * FROM users WHERE username = 'invitado'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("invitado", self._hash_password("user123"), "user")
                )
            
            conn.commit()

    # --- Gestión de Usuarios ---

    def register_user(self, username, password, role='user'):
        hashed_pw = self._hash_password(password)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed_pw, role)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print("El usuario ya existe.")
            return False
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def authenticate(self, username, password):
        hashed_pw = self._hash_password(password)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, api_key FROM users WHERE username = ? AND password = ?",
                (username, hashed_pw)
            )
            result = cursor.fetchone()
            if result:
                return {"role": result[0], "api_key": result[1]}
            return None

    def get_all_users(self):
        """Recupera todos los usuarios registrados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            return cursor.fetchall()

    def delete_user(self, username):
        """Elimina un usuario por su nombre de usuario."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    def save_user_api_key(self, username, api_key):
        """Guarda permanentemente la API KEY para un usuario."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET api_key = ? WHERE username = ?",
                    (api_key, username)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al guardar API Key: {e}")
            return False

    # --- Gestión de Base de Conocimiento (Especies) ---
    
    def add_species(self, genus, species, common_name, description, features, image_path=""):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO species (genus, species, common_name, description, key_features, image_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (genus, species, common_name, description, features, image_path))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al añadir especie: {e}")
            return False

    def get_all_species(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM species")
            return cursor.fetchall()

    def delete_species(self, species_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM species WHERE id = ?", (species_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar especie: {e}")
            return False

    def update_species(self, species_id, genus, species, common_name, description, features, image_path=None):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if image_path:
                    cursor.execute('''
                        UPDATE species 
                        SET genus = ?, species = ?, common_name = ?, description = ?, key_features = ?, image_path = ?
                        WHERE id = ?
                    ''', (genus, species, common_name, description, features, image_path, species_id))
                else:
                    cursor.execute('''
                        UPDATE species 
                        SET genus = ?, species = ?, common_name = ?, description = ?, key_features = ?
                        WHERE id = ?
                    ''', (genus, species, common_name, description, features, species_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar especie: {e}")
            return False

# Instancia global para ser usada por los controladores
db = Database()
