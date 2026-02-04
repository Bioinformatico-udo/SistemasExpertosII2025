""" **************************
    ***  AI_ASSISTANT.PY   *** 
    ************************** """
# Este archivo es el asistente de IA que se encarga de responder las preguntas de los usuarios.
# --- Importaciones ---
from groq import Groq
import os

# --- Clase AIAssistant ---
class AIAssistant:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Error al inicializar Groq: {e}")
                self.client = None
        else:
            self.client = None

    # --- Métodos de explicación taxonómica ---
    def get_taxonomic_explanation(self, species_name, common_name, detected_features):
        """Genera una explicación experta sobre por qué se llegó a esa identificación usando Groq."""
        if not self.client:
            return "Asistente IA (Groq) no configurado. Por favor, añada su API KEY de Groq."

        prompt = f"""
        Actúa como un experto mundial en taxonomía de la familia Hippidae (cangrejos topo).
        Se ha identificado un espécimen como: {species_name} ({common_name}).
        Rasgos: {detected_features}
        
        Da una breve explicación científica (máximo 3 líneas) sobre este hallazgo.
        Responde en español, sé directo y profesional.
        """
        
        try:
            # Usamos llama-3.3-70b-versatile o mixtral-8x7b-32768 que son muy estables en Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un biólogo experto en crustáceos decápodos."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            # Intentar con un modelo alternativo si el primero falla
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="mixtral-8x7b-32768",
                )
                return chat_completion.choices[0].message.content
            except:
                return f"Error en Groq: {str(e)}"

    # --- Métodos de consulta interactiva ---
    def chat_query(self, user_question, context_info=""):
        """Permite al usuario hacer preguntas libres al experto, limitando el alcance."""
        if not self.client:
            return "Asistente Groq no configurado."

        # Prompt Maestro: El "Cerebro" de SEITH
        system_prompt = """
        Eres el Profesor Experto del sistema SEITH (Sistema Experto de Identificación de Taxones de Hippidae). 
        Tu única especialidad es la biología marina, específicamente los decápodos de la familia Hippidae.
        
        REGLAS DE ORO:
        1. SOLO respondes sobre temas relacionados con cangrejos topo (Muy Muy), biología marina o SEITH.
        2. Si el usuario pregunta algo fuera de tema (política, deportes, programación general, etc.), debes 
        responder educadamente que como experto de SEITH, tu conocimiento se limita a la carcinología.
        3. Usa un tono académico, amable y motivador para los estudiantes.
        4. Si hay un diagnóstico previo, úsalo para dar detalles específicos.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Contexto del hallazgo: {context_info}\nPregunta del estudiante: {user_question}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error en la conversación: {str(e)}"
