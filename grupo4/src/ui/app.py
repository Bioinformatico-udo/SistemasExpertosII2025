"""Interfaz gráfica para el Sistema Experto de Porcelánidos de Venezuela.

Permite la identificación taxonómica mediante dos modos de inferencia:
1. Encadenamiento Hacia Adelante (Forward): Identificación abierta.
2. Encadenamiento Hacia Atrás (Backward): Verificación de hipótesis.
"""

import customtkinter as ctk
from pathlib import Path
from ..motor_reglas.reglas import reglas_iniciales, obtener_especies_disponibles
from ..motor_reglas.motor import evaluar_reglas, verificar_especie
from ..configuracion import MODEL_PATH
from ..ml.modelo import ModeloML
import pandas as pd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AplicacionPorcellanidos(ctk.CTk):
    """Aplicación principal para identificar porcelánidos venezolanos."""

    def __init__(self, rule_list=None, ml_model_path: str = None):
        super().__init__()
        self.title("Sistema Experto: Porcelánidos de Venezuela 🇻🇪🦀")
        self.geometry("1000x650") # Reducido para pantallas más pequeñas
        
        # Configuración de grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.rule_list = rule_list or reglas_iniciales()
        self.especies_disponibles = obtener_especies_disponibles()
        self.ml = None
        if ml_model_path:
            try:
                self.ml = ModeloML(ml_model_path)
            except Exception:
                self.ml = None
                
        # Registrar validador numérico
        self.validate_cmd = (self.register(self._validate_number), '%P')
        self._crear_widgets()

    def _validate_number(self, new_value):
        """Permite solo números y un punto decimal."""
        if new_value == "": return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def _crear_widgets(self):
        # --- Panel Izquierdo: Formulario ---
        self.frame_form = ctk.CTkFrame(self, width=320, corner_radius=15)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_form.grid_propagate(False)

        self.label_title = ctk.CTkLabel(
            self.frame_form, 
            text="Datos del Espécimen", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_title.pack(pady=(15, 5))

        # Sección: Modo de Inferencia
        self.frame_mode = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_mode.pack(fill="x", padx=10, pady=2)
        
        self.label_mode = ctk.CTkLabel(self.frame_mode, text="Modo de Inferencia:", font=ctk.CTkFont(weight="bold"))
        self.label_mode.pack(anchor="w")
        
        self.mode_var = ctk.StringVar(value="forward")
        self.radio_forward = ctk.CTkRadioButton(
            self.frame_mode, 
            text="Hacia Adelante",
            variable=self.mode_var,
            value="forward",
            command=self._toggle_modo,
            height=20
        )
        self.radio_forward.pack(pady=2, anchor="w")
        
        self.radio_backward = ctk.CTkRadioButton(
            self.frame_mode,
            text="Hacia Atrás",
            variable=self.mode_var,
            value="backward",
            command=self._toggle_modo,
            height=20
        )
        self.radio_backward.pack(pady=2, anchor="w")

        # Sección: Especie Objetivo (Solo Backward)
        self.frame_target = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_target.pack(fill="x", padx=10, pady=2)

        self.label_especie = ctk.CTkLabel(self.frame_target, text="Hipótesis (Especie):")
        self.label_especie.pack(anchor="w")
        self.especie_objetivo_var = ctk.CTkComboBox(
            self.frame_target,
            values=self.especies_disponibles,
            state="disabled"
        )
        if self.especies_disponibles:
            self.especie_objetivo_var.set(self.especies_disponibles[0])
        self.especie_objetivo_var.pack(fill="x", pady=2)

        self._separator()

        # Sección: Medidas Morfométricas
        self.label_medidas = ctk.CTkLabel(self.frame_form, text="Morfometría (mm):", font=ctk.CTkFont(weight="bold"))
        self.label_medidas.pack(anchor="w", padx=15, pady=(5, 2))

        # Helper para crear entries validados
        def create_numeric_entry(placeholder):
            entry = ctk.CTkEntry(self.frame_form, placeholder_text=placeholder)
            entry.configure(validate="key", validatecommand=self.validate_cmd)
            return entry

        self.entry_carapace = create_numeric_entry("Longitud Caparazón")
        self.entry_carapace.pack(fill="x", padx=15, pady=3)
        
        self.entry_rostro = create_numeric_entry("Longitud Rostro")
        self.entry_rostro.pack(fill="x", padx=15, pady=3)
        
        self.entry_chela_len = create_numeric_entry("Longitud Quela")
        self.entry_chela_len.pack(fill="x", padx=15, pady=3)
        
        self.entry_chela_w = create_numeric_entry("Ancho Quela")
        self.entry_chela_w.pack(fill="x", padx=15, pady=3)

        self._separator()

        # Sección: Rasgos Categóricos
        self.label_rasgos = ctk.CTkLabel(self.frame_form, text="Rasgos Cualitativos:", font=ctk.CTkFont(weight="bold"))
        self.label_rasgos.pack(anchor="w", padx=15, pady=(5, 2))

        self.orn_var = ctk.CTkComboBox(
            self.frame_form, 
            values=["desconocido", "lisa", "rugosa"],
            state="readonly"
        )
        self.orn_var.set("desconocido")
        self.orn_var.pack(fill="x", padx=15, pady=3)

        self.forma_quela_var = ctk.CTkComboBox(
            self.frame_form, 
            values=["desconocido", "robusta", "delgada"],
            state="readonly"
        )
        self.forma_quela_var.set("desconocido")
        self.forma_quela_var.pack(fill="x", padx=15, pady=3)

        self.pleon_var = ctk.IntVar(value=0)
        self.pleon_checkbox = ctk.CTkCheckBox(self.frame_form, text="Pleon Plegado", variable=self.pleon_var)
        self.pleon_checkbox.pack(anchor="w", padx=15, pady=3)

        self.setae_var = ctk.IntVar(value=0)
        self.setae_checkbox = ctk.CTkCheckBox(self.frame_form, text="Setas (Pelos) Presentes", variable=self.setae_var)
        self.setae_checkbox.pack(anchor="w", padx=15, pady=3)

        # Botón de Acción
        self.btn_evaluar = ctk.CTkButton(
            self.frame_form, 
            text="ANALIZAR ESPÉCIMEN 🔍", 
            command=self.evaluar, 
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f538d", hover_color="#14375e"
        )
        self.btn_evaluar.pack(side="bottom", fill="x", padx=15, pady=15)

        # --- Panel Derecho: Resultados ---
        self.frame_result = ctk.CTkFrame(self, corner_radius=15)
        self.frame_result.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        self.label_res_title = ctk.CTkLabel(
            self.frame_result, 
            text="Resultados del Análisis", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_res_title.pack(pady=20)

        self.text_result = ctk.CTkTextbox(self.frame_result, font=ctk.CTkFont(family="Consolas", size=14))
        self.text_result.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        self.text_result.configure(state="disabled") # Solo lectura por defecto

        # Tags para colores en texto
        self.text_result.tag_config("header", foreground="#3B8ED0") # font no soportado en tag_config de CTkTextbox
        self.text_result.tag_config("subheader", foreground="gray")
        self.text_result.tag_config("success", foreground="#2CC985") # Verde
        self.text_result.tag_config("error", foreground="#E04F5F")   # Rojo
        self.text_result.tag_config("warning", foreground="#ECA522") # Naranja
        self.text_result.tag_config("link", foreground="#3B8ED0", underline=True)

    def _separator(self):
        sep = ctk.CTkFrame(self.frame_form, height=2, fg_color="gray30")
        sep.pack(fill="x", padx=10, pady=10)

    def _toggle_modo(self):
        if self.mode_var.get() == "backward":
            self.especie_objetivo_var.configure(state="readonly")
        else:
            self.especie_objetivo_var.configure(state="disabled")

    def evaluar(self):
        # Recolectar (igual que antes)
        try: carapace = float(self.entry_carapace.get())
        except: carapace = 0.0
        try: rostro = float(self.entry_rostro.get())
        except: rostro = 0.0
        try: chela_len = float(self.entry_chela_len.get())
        except: chela_len = 0.0
        try: chela_w = float(self.entry_chela_w.get())
        except: chela_w = 0.0

        record = {
            'longitud_caparazon_mm': carapace,
            'longitud_rostro_mm': rostro,
            'longitud_quela_mm': chela_len,
            'ancho_quela_mm': chela_w,
            'pleon_plegado': int(self.pleon_var.get()),
            'presencia_setas': int(self.setae_var.get()),
            'ornamentacion_caparazon': self.orn_var.get(),
            'forma_quela': self.forma_quela_var.get()
        }

        # Ratios
        record['ratio_rostro'] = (record['longitud_rostro_mm'] / record['longitud_caparazon_mm']) if record['longitud_caparazon_mm'] > 0 else 0
        record['ratio_quela'] = (record['longitud_quela_mm'] / record['ancho_quela_mm']) if record['ancho_quela_mm'] > 0 else 0

        self.text_result.configure(state="normal") # Habilitar escritura
        self.text_result.delete("0.0", "end")

        # Capa 1: Filtro de Sensatez Biológica
        limite_max = 100.0 # 10 cm es el límite para porcelánidos venezolanos
        if any(v < 0 for v in [carapace, rostro, chela_len, chela_w]):
            self.text_result.insert("end", "⚠️ ERROR DE DATOS\n", "error")
            self.text_result.insert("end", "Las medidas de un espécimen no pueden ser negativas.\n")
            self.text_result.configure(state="disabled")
            return

        if any(v > limite_max for v in [carapace, rostro, chela_len, chela_w]):
            self.text_result.insert("end", "⚠️ DATOS INCONSISTENTES\n", "error")
            self.text_result.insert("end", f"Se han detectado medidas mayores a {limite_max} mm.\n")
            self.text_result.insert("end", "Estos valores son físicamente imposibles para estas especies.\n")
            self.text_result.insert("end", "\nPor favor, verifique si ha ingresado demasiados ceros.\n")
            self.text_result.configure(state="disabled")
            return

        modo = self.mode_var.get()

        if modo == "forward":
            self.text_result.insert("end", "Modo: Encadenamiento Hacia Adelante\n", "header")
            self.text_result.insert("end", "Buscando coincidencias en base de conocimientos...\n\n", "subheader")
            
            candidatos = evaluar_reglas(record, self.rule_list)
            
            if candidatos:
                self.text_result.insert("end", "✅ Coincidencias Lógicas (Reglas):\n\n", "success")
                for i, c in enumerate(candidatos, 1):
                    self.text_result.insert("end", f"{i}. {c['species']} (Certeza: {c['score']})\n")
                    self.text_result.insert("end", f"   • Motivo: {c['justification']}\n")
                    if 'info_detallada' in c and c['info_detallada']:
                        self.text_result.insert("end", f"   • Ficha: {c['info_detallada']}\n")
                    if 'link_especie' in c and c['link_especie']:
                        self.text_result.insert("end", f"   • Más información: ", "subheader")
                        self.text_result.insert("end", f"{c['link_especie']}\n", "link")
                    self.text_result.insert("end", "\n")
            else:
                self.text_result.insert("end", "❌ Ninguna regla coincide exactamente.\n", "warning")
                self.text_result.insert("end", "Los datos no siguen un patrón biológico conocido.\n\n", "subheader")

            if self.ml:
                try:
                    # IA Humility check: Si no hay reglas, la IA debe ser cautelosa
                    if not candidatos:
                        self.text_result.insert("end", "⚠️ ADVERTENCIA DE IA:\n", "warning")
                        self.text_result.insert("end", "Los datos son sospechosos. La IA sugerirá algo, pero\n")
                        self.text_result.insert("end", "no existe respaldo biológico para este espécimen.\n\n")

                    # Preparar rasgos numéricos para la IA
                    orn_val = 1 if record['ornamentacion_caparazon'].lower() == 'rugosa' else 0
                    forma_val = 1 if record['forma_quela'].lower() == 'delgada' else 0

                    # Crear DF para ML con todas las características sincronizadas
                    df_input = pd.DataFrame([{
                        'ratio_rostro': record['ratio_rostro'],
                        'ratio_quela': record['ratio_quela'],
                        'longitud_caparazon_mm': record['longitud_caparazon_mm'],
                        'pleon_plegado': record['pleon_plegado'],
                        'presencia_setas': record['presencia_setas'],
                        'orn_numeric': orn_val,
                        'forma_numeric': forma_val
                    }])
                    # Predecir
                    probs = self.ml.predict_proba(df_input)
                    clases = self.ml.clases()
                    prob_list = list(zip(clases, probs[0]))
                    prob_list.sort(key=lambda x: x[1], reverse=True)
                    
                    self.text_result.insert("end", "🤖 Sugerencias de IA (Probabilísticas):\n\n", "header")
                    top3 = prob_list[:3]
                    for cls, p in top3:
                        if p > 0.01:
                            confianza = "Alta" if p > 0.7 else "Media" if p > 0.4 else "Baja"
                            color = "success" if p > 0.5 else "warning"
                            self.text_result.insert("end", f"  • {cls}: ", color)
                            self.text_result.insert("end", f"{p:.1%} (Confianza {confianza})\n")
                except Exception as e:
                    self.text_result.insert("end", f"\n⚠️ Error ML: {e}\n", "error")
            else:
                 self.text_result.insert("end", "\nℹ️ IA no disponible (modelo no cargado).\n")

        else:
            # BACKWARD
            especie = self.especie_objetivo_var.get()
            self.text_result.insert("end", "Modo: Encadenamiento Hacia Atrás\n", "header")
            self.text_result.insert("end", f"Verificando hipótesis: ¿Es {especie}?\n\n", "subheader")
            
            res = verificar_especie(record, especie, self.rule_list)
            
            if not res['regla_encontrada']:
                self.text_result.insert("end", f"⚠️ {res['mensaje']}\n", "warning")
            else:
                if res['verificada']:
                    self.text_result.insert("end", f"✅ CONDICIONES CUMPLIDAS\n", "success")
                else:
                    self.text_result.insert("end", f"❌ NO COINCIDE\n", "error")
                
                self.text_result.insert("end", f"\n{res['mensaje']}\n\n")
                self.text_result.insert("end", f"Justificación Biológica:\n{res['justification']}\n")
                
                # Ficha técnica adicional en Backward
                regla = res.get('regla_detalle', {})
                if res['verificada'] and regla:
                    if 'info_detallada' in regla:
                        self.text_result.insert("end", f"\nFicha Técnica:\n{regla['info_detallada']}\n")
                    if 'link_especie' in regla:
                        self.text_result.insert("end", f"\nEnlace de referencia:\n", "subheader")
                        self.text_result.insert("end", f"{regla['link_especie']}\n", "link")
                elif not res['verificada']:
                    self.text_result.insert("end", "\n⚠️ ADVERTENCIA: Los datos ingresados contradicen\n", "warning")
                    self.text_result.insert("end", f"la hipótesis de que el espécimen es {especie}.\n")
        
        self.text_result.configure(state="disabled") # Bloquear escritura nuevamente

if __name__ == "__main__":
    ml_path = MODEL_PATH if Path(MODEL_PATH).exists() else None
    app = AplicacionPorcellanidos(ml_model_path=ml_path)
    app.mainloop()
