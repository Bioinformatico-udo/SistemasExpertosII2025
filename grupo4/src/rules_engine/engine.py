"""Motor de evaluación de reglas con salida explicada."""

from typing import List, Dict

def evaluar_reglas(record: Dict, reglas: List[Dict]) -> List[Dict]:
    """Evalúa una lista de reglas sobre un registro y devuelve candidatos ordenados.

    Args:
        record: diccionario con campos del registro.
        reglas: lista de reglas (ver rules.py).

    Returns:
        Lista de candidatos con keys: species, score, matched, justification, rule_id.
    """
    candidatos = []
    for regla in reglas:
        condiciones = regla.get('conditions', [])
        match = 0
        for cond in condiciones:
            try:
                if cond(record):
                    match += 1
            except Exception:
                # Si una condición falla por datos faltantes, la tratamos como no cumplida
                continue
        score = match / len(condiciones) if condiciones else 0
        if score >= regla.get('threshold', 0.6):
            candidatos.append({
                'rule_id': regla.get('id'),
                'species': regla.get('species'),
                'score': round(score, 2),
                'matched': int(match),
                'justification': regla.get('justification')
            })
    candidatos.sort(key=lambda x: x['score'], reverse=True)
    return candidatos
