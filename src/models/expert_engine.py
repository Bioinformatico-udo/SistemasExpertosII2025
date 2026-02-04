""" ************************** 
    ***     EXPERT ENGINE    *** 
    ************************** """
# Este archivo contiene la clase ExpertEngine que se encarga de gestionar el motor de analisis de especies y su comprensión.

# --- Importaciones ---
from src.models.database import db
import json

# --- Clase principal ---
class ExpertEngine:
    # Inicializa el motor de inferencia
    def __init__(self):
        self.rules = []

    # Carga las reglas (especies) desde la base de datos
    def load_rules_from_db(self):
        """Carga las reglas (especies) desde la base de datos."""
        species_data = db.get_all_species()
        self.rules = []
        for s in species_data:
            # Intentamos parsear los rasgos como JSON, si falla los tratamos como texto
            try:
                features = json.loads(s[5])
            except:
                # Si es texto plano, lo convertimos en una lista de palabras clave
                features = s[5].lower().replace(",", " ").split()
            
            self.rules.append({
                "genus": s[1],
                "species": s[2],
                "common_name": s[3],
                "features": features
            })

    # Identifica las especies por rasgos
    def identify_by_features(self, user_features):
        """
        Motor de inferencia con Ponderación de Rasgos (Calidad sobre Cantidad).
        user_features puede ser una lista de rasgos seleccionados.
        """
        self.load_rules_from_db()
        results = []
        
        thesaurus = {
            "subcilindrico": ["ovalado", "cilindrico", "alargado"],
            "ovalado": ["subcilindrico", "redondeado", "elipsoide"],
            "liso": ["suave", "sin rugosidad"],
            "rugoso": ["granulado", "estriado", "asperos", "rugosa"]
        }

        # Asegurar que user_features sea una lista limpia
        if isinstance(user_features, str):
            user_features = [f.strip().lower() for f in user_features.replace(",", " ").split() if f.strip()]
        else:
            user_features = [f.lower() for f in user_features if f.lower() != "no observado"]
        
        if not user_features: return []

        for rule in self.rules:
            score = 0
            rule_features = [f.strip().lower() for f in rule["features"]]
            
            for u_feat in user_features:
                # Rasgos con Mayor Peso Taxonómico
                weight = 1.5 if any(k in u_feat for k in ["rugoso", "falcado", "estriado"]) else 1.0
                
                # Coincidencia Directa
                found = False
                if u_feat in rule_features:
                    score += weight
                    found = True
                else:
                    # Coincidencia Parcial (Ej: 'rugoso' coincide en 'caparazon rugoso')
                    for r_feat in rule_features:
                        if u_feat in r_feat or r_feat in u_feat:
                            score += weight
                            found = True
                            break
                
                # Coincidencia por Tesauro
                if not found and u_feat in thesaurus:
                    for syn in thesaurus[u_feat]:
                        if any(syn in r_f for r_f in rule_features):
                            score += (weight * 0.7)
                            found = True
                            break
            
            if score > 0:
                # Probabilidad basada en la cantidad de rasgos coincidentes sobre los buscados
                probability = (score / len(user_features)) * 100
                probability = min(probability, 100) # Cap at 100%

                results.append({
                    "genus": rule["genus"],
                    "species": rule["species"],
                    "common_name": rule["common_name"],
                    "probability": round(probability, 2)
                })
        
        return sorted(results, key=lambda x: x["probability"], reverse=True)

# Instancia global
engine = ExpertEngine()
