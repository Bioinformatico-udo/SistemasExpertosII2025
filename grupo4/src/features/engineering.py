"""Funciones para crear features KommonCats usadas por reglas y ML."""

import pandas as pd

def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Selecciona y codifica features para el modelo.

    - Normaliza categorías simples.
    - Devuelve DataFrame listo para entrenamiento/predicción.
    """
    df = df.copy()

    # Asegurar columnas binarias
    if 'pleon_folded' in df.columns:
        df['pleon_folded'] = df['pleon_folded'].fillna(0).astype(int)
    else:
        df['pleon_folded'] = 0

    if 'setae_presence' in df.columns:
        df['setae_presence'] = df['setae_presence'].fillna(0).astype(int)
    else:
        df['setae_presence'] = 0

    # Categorías
    df['carapace_ornamentation'] = df.get('carapace_ornamentation', 'unknown').fillna('unknown')
    df['chela_shape'] = df.get('chela_shape', 'unknown').fillna('unknown')

    # Ratios (si no existen, se asume 0)
    df['rostro_ratio'] = df.get('rostro_ratio', 0).fillna(0)
    df['chela_ratio'] = df.get('chela_ratio', 0).fillna(0)

    return df
