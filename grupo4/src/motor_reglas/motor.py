"""Motor de evaluación de reglas.

Este módulo expone dos estrategias de inferencia para sistemas expertos:

1. **Encadenamiento hacia adelante (Forward Chaining)**: `evaluar_reglas()`
   - Parte de los datos conocidos y evalúa TODAS las reglas disponibles.
   - Devuelve TODAS las especies candidatas con sus scores.
   - Útil cuando no se tiene hipótesis previa (identificación abierta).

2. **Encadenamiento hacia atrás (Backward Chaining)**: `verificar_especie()`
   - Parte de una especie objetivo (hipótesis) y verifica si los datos
     la soportan.
   - Devuelve evidencia a favor o en contra de esa especie específica.
   - Útil para confirmar/rechazar una hipótesis taxonómica.

Formato esperado de una regla (ejemplo):
{
    'id': 'R_X',
    'species': 'Propuesta sp. X',
    'conditions': [callable, callable, ...],
    'justification': 'Texto explicativo',
    'threshold': 0.66
}

La función intenta evaluar cada condición y contabiliza las que devuelven
True. El `score` se calcula como la fracción de condiciones satisfechas. Si
ese `score` es >= `threshold` de la regla, la regla se añade a la lista de
candidatos.
"""

from typing import List, Dict, Optional


def evaluar_reglas(record: Dict, reglas: List[Dict]) -> List[Dict]:
    """Evalúa `reglas` sobre un `record` y devuelve candidatos ordenados.

    Args:
        record: Diccionario o mapping con las características del espécimen.
        reglas: Lista de reglas en el formato documentado arriba.

    Returns:
        Lista de diccionarios, cada uno con las claves:
        - `rule_id`: id de la regla que coincidió.
        - `species`: especie propuesta por la regla.
        - `score`: fracción de condiciones satisfechas (redondeada a 2 decimales).
        - `matched`: número entero de condiciones satisfechas.
        - `justification`: texto explicativo de la regla.

    Notas:
        - Si una condición lanza una excepción se ignora esa condición (no
          cuenta como cumplida). Esto evita que valores faltantes rompan la
          evaluación, pero puede ocultar errores en las funciones de condición.
        - El resultado está ordenado por `score` descendente.

    Ejemplo:
        >>> # Suponiendo que reglas es una lista de reglas válidas
        >>> evaluar_reglas({'ratio_rostro': 0.35}, reglas)
        [{'rule_id': '...', 'species': '...', 'score': 0.67, ...}]
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
                # Ignorar errores en la evaluación de condiciones para evitar
                # fallos por datos incompletos; el usuario puede querer
                # inspeccionar logs o validar entradas antes de la evaluación.
                continue
        score = match / len(condiciones) if condiciones else 0
        if score >= regla.get('threshold', 0.6):
            candidatos.append({
                'rule_id': regla.get('id'),
                'species': regla.get('species'),
                'score': round(score, 2),
                'matched': int(match),
                'justification': regla.get('justification'),
                'info_detallada': regla.get('info_detallada'),
                'link_especie': regla.get('link_especie')
            })
    candidatos.sort(key=lambda x: x['score'], reverse=True)
    return candidatos


def buscar_regla_por_especie(especie: str, reglas: List[Dict]) -> Optional[Dict]:
    """Busca la regla que propone una especie específica.

    Args:
        especie: Nombre de la especie objetivo (ej. 'Porcellana sp. A').
        reglas: Lista de reglas disponibles.

    Returns:
        La primera regla que coincida con la especie, o None si no existe.

    Nota:
        La comparación es case-insensitive y elimina espacios en blanco
        para mayor flexibilidad.
    """
    especie_normalizada = especie.strip().lower()
    for regla in reglas:
        if regla.get('species', '').strip().lower() == especie_normalizada:
            return regla
    return None


def verificar_especie(record: Dict, especie_objetivo: str, reglas: List[Dict]) -> Dict:
    """Encadenamiento hacia atrás: Verifica si los datos soportan una especie.

    Esta función implementa **backward chaining** (razonamiento dirigido por
    objetivos). En lugar de evaluar todas las reglas, busca la regla específica
    de la especie objetivo y verifica si las condiciones se cumplen.

    Args:
        record: Diccionario con las características del espécimen.
        especie_objetivo: Nombre de la especie a verificar (hipótesis).
        reglas: Lista de reglas disponibles.

    Returns:
        Diccionario con las claves:
        - `especie`: nombre de la especie objetivo.
        - `verificada`: bool indicando si se cumple el threshold.
        - `score`: fracción de condiciones satisfechas (0.0 a 1.0).
        - `condiciones_totales`: número de condiciones en la regla.
        - `condiciones_cumplidas`: número de condiciones que pasaron.
        - `condiciones_faltantes`: número de condiciones no cumplidas.
        - `justification`: texto explicativo de la regla.
        - `mensaje`: descripción del resultado de la verificación.
        - `regla_encontrada`: bool indicando si existe una regla para la especie.

    Ejemplo:
        >>> # reglas = reglas_iniciales()
        >>> verificar_especie(
        ...     {'ratio_rostro': 0.26, ...},
        ...     'Pisidia brasiliensis',
        ...     reglas
        ... )
        {
            'especie': 'Pisidia brasiliensis',
            'verificada': True,
            'score': 1.0,
            'condiciones_totales': 3,
            'condiciones_cumplidas': 3,
            'condiciones_faltantes': 0,
            'justification': '...',
            'mensaje': 'La hipótesis es VERDADERA ...'
        }

    Notas:
        - Si no existe una regla para la especie, devuelve un resultado
          indicando que no se pudo verificar.
        - Si una condición lanza una excepción, se cuenta como no cumplida.
        - Este es el método apropiado cuando ya tienes una hipótesis
          taxonómica y quieres confirmarla o descartarla.
    """
    # Buscar la regla específica para la especie objetivo
    regla = buscar_regla_por_especie(especie_objetivo, reglas)

    if regla is None:
        return {
            'especie': especie_objetivo,
            'verificada': False,
            'score': 0.0,
            'condiciones_totales': 0,
            'condiciones_cumplidas': 0,
            'condiciones_faltantes': 0,
            'justification': '',
            'mensaje': f'No existe una regla definida para "{especie_objetivo}".',
            'regla_encontrada': False
        }

    # Evaluar las condiciones de la regla encontrada
    condiciones = regla.get('conditions', [])
    threshold = regla.get('threshold', 0.6)
    justification = regla.get('justification', '')

    match = 0
    for cond in condiciones:
        try:
            if cond(record):
                match += 1
        except Exception:
            # Condición no cumplida por error (datos faltantes, etc.)
            continue

    total = len(condiciones)
    score = match / total if total > 0 else 0
    faltantes = total - match
    verificada = score >= threshold

    # Construir mensaje explicativo
    if verificada:
        mensaje = (
            f'La hipótesis es VERDADERA: "{especie_objetivo}" cumple el threshold '
            f'({score:.0%} >= {threshold:.0%}). '
            f'{match} de {total} condiciones satisfechas.'
        )
    else:
        mensaje = (
            f'La hipótesis es FALSA: "{especie_objetivo}" NO cumple el threshold '
            f'({score:.0%} < {threshold:.0%}). '
            f'Solo {match} de {total} condiciones satisfechas, faltan {faltantes}.'
        )

    return {
        'especie': especie_objetivo,
        'verificada': verificada,
        'score': score,
        'condiciones_totales': total,
        'condiciones_cumplidas': match,
        'condiciones_faltantes': faltantes,
        'justification': regla.get('justification', ''),
        'mensaje': mensaje,
        'regla_encontrada': True,
        'regla_detalle': regla # Devolvemos la regla completa para acceder a info y links
    }
