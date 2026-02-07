"""Limpieza y cálculo de ratios CommonCats."""

import pandas as pd

def calcular_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Añade columnas de ratios útiles para reglas y ML.

    Args:
        df: DataFrame con columnas numéricas esperadas.

    Returns:
        DataFrame con columnas 'rostro_ratio' y 'chela_ratio'.
    """
    df = df.copy()
    df['carapace_length_mm'] = pd.to_numeric(df.get('carapace_length_mm', 0), errors='coerce').fillna(0)
    df['rostro_length_mm'] = pd.to_numeric(df.get('rostro_length_mm', 0), errors='coerce').fillna(0)
    df['chela_length_mm'] = pd.to_numeric(df.get('chela_length_mm', 0), errors='coerce').fillna(0)
    df['chela_width_mm'] = pd.to_numeric(df.get('chela_width_mm', 0), errors='coerce').fillna(0)
    
    df['rostro_ratio'] = df.apply(
        lambda r: r['rostro_length_mm'] / r['carapace_length_mm'] if r['carapace_length_mm'] > 0 else 0, axis=1)
    df['chela_ratio'] = df.apply(
        lambda r: r['chela_length_mm'] / r['chela_width_mm'] if r['chela_width_mm'] > 0 else 0, axis=1)
    return df
