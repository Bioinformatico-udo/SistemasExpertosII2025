"""Interfaz básica con CustomTkinter (esqueleto).

Formulario simple para ingresar medidas y evaluar reglas/ML.
"""

import customtkinter as ctk
from pathlib import Path
from ..rules_engine.rules import reglas_iniciales
from ..rules_engine.engine import evaluar_reglas
from ..config import IMAGE_STORAGE_PATH, MODEL_PATH
from ..ml.model import MLModel
import pandas as pd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PorcellanidsApp(ctk.CTk):
    """Aplicación principal para evaluar registros KommonCats."""

    def __init__(self, rule_list=None, ml_model_path: str = None):
        super().__init__()
        self.title("Identificador de Porcelánidos - KommonCats")
        self.geometry("1000x650")
        self.rule_list = rule_list or reglas_iniciales()
        self.ml = None
        if ml_model_path:
            try:
                self.ml = MLModel(ml_model_path)
            except Exception:
                self.ml = None
        self._crear_widgets()

    def _crear_widgets(self):
        # Panel izquierdo: formulario
        self.frame_form = ctk.CTkFrame(self, width=340)
        self.frame_form.pack(side="left", fill="y", padx=10, pady=10)

        self.label_title = ctk.CTkLabel(self.frame_form, text="Ingresar medidas y rasgos", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.pack(pady=6)

        self.entry_carapace = ctk.CTkEntry(self.frame_form, placeholder_text="Longitud caparazón (mm)")
        self.entry_carapace.pack(pady=6)
        self.entry_rostro = ctk.CTkEntry(self.frame_form, placeholder_text="Longitud rostro (mm)")
        self.entry_rostro.pack(pady=6)
        self.entry_chela_len = ctk.CTkEntry(self.frame_form, placeholder_text="Longitud quela (mm)")
        self.entry_chela_len.pack(pady=6)
        self.entry_chela_w = ctk.CTkEntry(self.frame_form, placeholder_text="Ancho quela (mm)")
        self.entry_chela_w.pack(pady=6)

        self.pleon_var = ctk.IntVar(value=0)
        self.pleon_checkbox = ctk.CTkCheckBox(self.frame_form, text="Pleon plegado", variable=self.pleon_var)
        self.pleon_checkbox.pack(pady=6)

        self.setae_var = ctk.IntVar(value=0)
        self.setae_checkbox = ctk.CTkCheckBox(self.frame_form, text="Setas presentes", variable=self.setae_var)
        self.setae_checkbox.pack(pady=6)

        self.orn_var = ctk.CTkComboBox(self.frame_form, values=["unknown","smooth","tuberculate","keeled"])
        self.orn_var.set("unknown")
        self.orn_var.pack(pady=6)
        self.chela_shape_var = ctk.CTkComboBox(self.frame_form, values=["unknown","slender","robust"])
        self.chela_shape_var.set("unknown")
        self.chela_shape_var.pack(pady=6)

        self.btn_evaluar = ctk.CTkButton(self.frame_form, text="Evaluar", command=self.evaluar)
        self.btn_evaluar.pack(pady=12)

        # Panel derecho: resultados
        self.frame_result = ctk.CTkFrame(self)
        self.frame_result.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.text_result = ctk.CTkTextbox(self.frame_result)
        self.text_result.pack(expand=True, fill="both")

    def evaluar(self):
        # Recolectar inputs y construir registro simple
        try:
            carapace = float(self.entry_carapace.get())
        except:
            carapace = 0.0
        try:
            rostro = float(self.entry_rostro.get())
        except:
            rostro = 0.0
        try:
            chela_len = float(self.entry_chela_len.get())
            chela_w = float(self.entry_chela_w.get())
        except:
            chela_len = 0.0
            chela_w = 0.0

        record = {
            'carapace_length_mm': carapace,
            'rostro_length_mm': rostro,
            'chela_length_mm': chela_len,
            'chela_width_mm': chela_w,
            'pleon_folded': int(self.pleon_var.get()),
            'setae_presence': int(self.setae_var.get()),
            'carapace_ornamentation': self.orn_var.get(),
            'chela_shape': self.chela_shape_var.get()
        }
        # Calcular ratios simples
        record['rostro_ratio'] = (record['rostro_length_mm'] / record['carapace_length_mm']) if record['carapace_length_mm'] > 0 else 0
        record['chela_ratio'] = (record['chela_length_mm'] / record['chela_width_mm']) if record['chela_width_mm'] > 0 else 0

        # Evaluar reglas
        candidatos = evaluar_reglas(record, self.rule_list)
        self.text_result.delete("0.0", "end")
        if candidatos:
            self.text_result.insert("end", "Candidatos por reglas:\n\n")
            for c in candidatos:
                self.text_result.insert("end", f"{c['species']} (score: {c['score']})\nJustificación: {c['justification']}\n\n")
        else:
            self.text_result.insert("end", "No se encontraron coincidencias por reglas.\n")

        # Si hay modelo ML, usar como fallback
        if self.ml:
            try:
                import pandas as pd
                X = pd.DataFrame([{
                    'rostro_ratio': record['rostro_ratio'],
                    'chela_ratio': record['chela_ratio'],
                    'pleon_folded': record['pleon_folded'],
                    'setae_presence': record['setae_presence']
                }])
                probs = self.ml.predict_proba(X)
                clases = self.ml.clases()
                # ordenar por probabilidad
                prob_list = list(zip(clases, probs[0]))
                prob_list.sort(key=lambda x: x[1], reverse=True)
                self.text_result.insert("end", "Candidatos por ML (fallback):\n\n")
                for cls, p in prob_list[:5]:
                    self.text_result.insert("end", f"{cls} (prob: {p:.2f})\n")
            except Exception as e:
                self.text_result.insert("end", f"Error al usar ML: {e}\n")
        else:
            self.text_result.insert("end", "\nModelo ML no cargado. Entrena y guarda el modelo en la ruta configurada para usarlo como fallback.\n")

if __name__ == "__main__":
    # Intentar cargar modelo si existe
    ml_path = MODEL_PATH if Path(MODEL_PATH).exists() else None
    app = PorcellanidsApp(ml_model_path=ml_path)
    app.mainloop()
