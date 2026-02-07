"""Definición de reglas taxonómicas iniciales (documentadas en español).

Cada regla es un diccionario con:
- id: identificador único
- species: especie propuesta (texto)
- conditions: lista de funciones que reciben un registro (dict o Series) y devuelven True/False
- justification: explicación en español
- threshold: proporción mínima de condiciones que deben cumplirse para aceptar la regla
"""

def regla_porcellana_A():
    return {
        'id': 'R_PORC_A',
        'species': 'Porcellana sp. A',
        'conditions': [
            lambda r: float(r.get('rostro_ratio', 0)) > 0.30,
            lambda r: str(r.get('chela_shape', '')).lower() == 'slender',
            lambda r: int(r.get('pleon_folded', 0)) == 1
        ],
        'justification': 'Rostro relativamente largo, quelas delgadas y pleon plegado.',
        'threshold': 0.66
    }

def regla_petrolisthes_B():
    return {
        'id': 'R_PETR_B',
        'species': 'Petrolisthes sp. B',
        'conditions': [
            lambda r: str(r.get('carapace_ornamentation', '')).lower() == 'smooth',
            lambda r: str(r.get('chela_shape', '')).lower() == 'robust',
            lambda r: int(r.get('rostro_spines_count', 0)) == 0
        ],
        'justification': 'Caparazón liso, quelas robustas y rostro sin espinas.',
        'threshold': 0.66
    }

def reglas_iniciales():
    """Devuelve la lista de reglas iniciales documentadas."""
    return [regla_porcellana_A(), regla_petrolisthes_B()]
