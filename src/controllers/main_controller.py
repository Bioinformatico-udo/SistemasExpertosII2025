""" ************************** 
    ***   MAIN CONTROLLER  *** 
    ************************** """
# Este controlador es el encargado de gestionar la lógica de la aplicación.

# --- Importaciones ---
import os
from PIL import Image
from src.models.database import db
from src.models.expert_engine import ExpertEngine
from src.utils.image_helper import ImageHelper
from src.utils.ai_assistant import AIAssistant

# --- Clase MainController ---
class MainController:
    # --- Inicialización ---
    def __init__(self):
        self.engine = ExpertEngine()
        self.image_helper = ImageHelper
        self.ai = AIAssistant() # Inicializa el asistente

    # --- Métodos de autenticación ---
    def login(self, username, password):
        user_info = db.authenticate(username, password)
        if user_info:
            self.current_user = username
            self.user_api_key = user_info.get("api_key")
            return user_info.get("role")
        return None

    # --- Métodos de registro ---
    def register(self, username, password):
        return db.register_user(username, password)

    # --- Métodos de API Key ---
    def save_api_key(self, api_key):
        """Guarda la API Key en el perfil del usuario actual."""
        if hasattr(self, 'current_user'):
            return db.save_user_api_key(self.current_user, api_key)
        return False

    # --- Lógica de Identificación (Usuario) ---
    def identify_specimen(self, image_path):
        """Orquesta el proceso de visión y motor experto."""
        # 1. Visión por Computadora (Asistencia)
        analysis = self.image_helper.process_image(image_path)
        
        if analysis and analysis["status"] == "success":
            detected_shape = analysis["detected_shape"]
            # 2. Inferencia del Motor Experto (Buchanan)
            results = self.engine.identify_by_features(detected_shape)
            
            # 3. Enriquecer resultados con rutas de imagen de la DB
            all_species = db.get_all_species()
            species_map = {f"{s[1]} {s[2]}": s[6] for s in all_species}
            
            for res in results:
                key = f"{res['genus']} {res['species']}"
                res["ref_image"] = species_map.get(key, "")

            return {
                "status": "success",
                "analysis": analysis,
                "results": results
            }
        return {"status": "error", "message": "No se detectaron rasgos claros"}

    # --- Métodos de identificación manual (Nueva Lógica de Categorización) ---
    def identify_by_manual_selection(self, traits_list):
        """Identifica especies basándose exclusivamente en una lista de rasgos seleccionados."""
        results = self.engine.identify_by_features(traits_list)
        
        # Enriquecer con imágenes de referencia
        all_species = db.get_all_species()
        species_map = {f"{s[1]} {s[2]}": s[6] for s in all_species}
        for res in results:
            key = f"{res['genus']} {res['species']}"
            res["ref_image"] = species_map.get(key, "")
            
        return results

    # --- Gestión de Usuarios (Reestructuración) ---
    def get_all_users(self):
        """Recupera la lista de usuarios registrados."""
        return db.get_all_users()

    def delete_user(self, username):
        """Elimina un usuario (seguridad)."""
        if username == "admin": return False
        return db.delete_user(username)

    # --- Métodos de generación de reportes ---
    def generate_id_report(self, user_image_path, result_data, ai_conversation=""):
        """Genera un certificado PDF con el resultado de la identificación, incluyendo el chat de la IA."""
        from fpdf import FPDF
        from datetime import datetime
        import pathlib
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Colores SEITH
        pdf.set_text_color(0, 102, 102) # Cian oscuro
        
        # Título y Header
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(0, 20, "SEITH - REPORTE CIENTIFICO", ln=True, align="C")
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 10, f"Fecha de emision: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        
        # 1. Registro Visual
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(240, 255, 255)
        pdf.cell(0, 10, " 1. ANALISIS DE VISION ARTIFICIAL", ln=True, fill=True)
        pdf.ln(5)
        
        if os.path.exists(user_image_path):
            # Centrar imagen
            pdf.image(user_image_path, x=55, w=100)
            pdf.ln(5)

        # 2. Diagnostico Experto
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, " 2. DIAGNOSTICO DEL SISTEMA EXPERTO", ln=True, fill=True)
        pdf.ln(5)
        
        if result_data:
            top_result = result_data[0]
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(0, 153, 153)
            pdf.cell(0, 10, f"Especie: {top_result['genus']} {top_result['species']}", ln=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(80, 10, f"Nombre Comun: {top_result['common_name']}")
            pdf.cell(0, 10, f"Precision: {top_result['probability']}%", ln=True)
            
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 7, f"Basado en los rasgos detectados y verificados manualmente, el sistema experto ha determinado con un alto grado de confianza la coincidencia con {top_result['genus']} {top_result['species']}.")

        # 3. Anexo: Consultoria con IA (Groq/Expert)
        if ai_conversation and len(ai_conversation.strip()) > 50:
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(0, 10, " 3. ANEXO: SUSTENTO DEL ORIENTADOR IA", ln=True, fill=True)
            pdf.ln(5)
            
            pdf.set_font("Helvetica", "", 9)
            
            # Limpieza Quirúrgica: Eliminamos Emojis y caracteres no compatibles con el PDF estándar
            # Reemplazamos los encabezados del chat por etiquetas limpias
            clean_conv = ai_conversation.replace("👤 Estudiante:", "[ESTUDIANTE]:")
            clean_conv = clean_conv.replace("🤖 Experto SEITH:", "[EXPERTO]:")
            clean_conv = clean_conv.replace("🤖 Bienvenido", "Bienvenido")
            
            # Forzamos codificación limpia (Elimina cualquier emoji residual del LLM)
            clean_conv = clean_conv.encode('latin-1', 'ignore').decode('latin-1')
            
            pdf.multi_cell(0, 6, clean_conv)

        # Guardar en Descargas
        downloads_path = str(pathlib.Path.home() / "Downloads")
        filename = f"SEITH_Reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(downloads_path, filename)
        
        pdf.output(output_path)
        return output_path

    # --- Lógica de Administración (Conocimiento) ---
    def get_all_species(self):
        return db.get_all_species()

    # --- Administración de Especies ---
    def add_species(self, genus, species, common_name, description, features, image_path=None):
        saved_path = ""
        if image_path and os.path.exists(image_path):
            filename = f"{genus}_{species}.png".replace(" ", "_").lower()
            saved_path = os.path.join("assets", "species_images", filename)
            abs_saved_path = os.path.join(os.getcwd(), saved_path)
            # Guardamos la imagen
            with Image.open(image_path) as img:
                img.save(abs_saved_path)
                
        return db.add_species(genus, species, common_name, description, features, saved_path)

    # --- Métodos de actualización de especies ---
    def update_species(self, species_id, genus, species, common_name, description, features, image_path=None):
        saved_path = None
        if image_path and os.path.exists(image_path):
            filename = f"{genus}_{species}_{species_id}.png".replace(" ", "_").lower()
            saved_path = os.path.join("assets", "species_images", filename)
            abs_saved_path = os.path.join(os.getcwd(), saved_path)
            with Image.open(image_path) as img:
                img.save(abs_saved_path)
        
        return db.update_species(species_id, genus, species, common_name, description, features, saved_path)

    # --- Métodos de eliminación de especies ---
    def delete_species(self, species_id):
        return db.delete_species(species_id)

    # --- Lógica de IA Generativa ---
    def set_ai_api_key(self, api_key):
        """Permite configurar la llave de Gemini en tiempo de ejecución."""
        self.ai = AIAssistant(api_key=api_key)
        return True

    # --- Métodos de explicación de IA ---
    def get_ai_explanation(self, result):
        """Obtiene una explicación científica sobre el resultado."""
        if not result or len(result) == 0:
            return "No hay resultados para explicar."
        
        top = result[0]
        # Creamos un resumen de rasgos para el prompt
        features_desc = f"Forma caparazón Detectado: {top.get('probability')}% match."
        
        return self.ai.get_taxonomic_explanation(
            f"{top['genus']} {top['species']}", 
            top['common_name'], 
            features_desc
        )

    # --- Métodos de chat interactivo ---
    def chat_with_ai(self, question, results):
        """Conversación interactiva con contexto."""
        context = ""
        if results and len(results) > 0:
            top = results[0]
            context = f"El usuario está viendo un {top['genus']} {top['species']}."
        
        return self.ai.chat_query(question, context)
