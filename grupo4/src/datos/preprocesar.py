"""Limpieza y cálculo de ratios CommonCats (versión en español).

Proporciona utilidades sencillas para convertir columnas a numérico y calcular
ratios morfológicos usados por el motor de reglas y el ML.
"""

import pandas as pd


def calcular_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Añade columnas numéricas y calcula ratios relevantes.

    Transforma las columnas de longitud/ancho a tipo numérico y crea dos
    columnas nuevas:
    - `ratio_rostro` = longitud_rostro_mm / longitud_caparazon_mm
    - `ratio_quela` = longitud_quela_mm / ancho_quela_mm

    Los cálculos manejan divisiones por cero devolviendo 0 cuando falta el
    denominador.

    Args:
        df: DataFrame que contiene (al menos) las columnas de longitudes y anchos.

    Returns:
        Copia del DataFrame con las columnas numéricas y los ratios añadidos.

    Ejemplo:
        >>> import pandas as pd
        >>> df = pd.DataFrame([{ 'longitud_caparazon_mm':10, 'longitud_rostro_mm':3, 'longitud_quela_mm':12, 'ancho_quela_mm':4 }])
        >>> out = calcular_ratios(df)
        >>> out['ratio_rostro'].iloc[0]
        0.3
    """
    df = df.copy()
    df['longitud_caparazon_mm'] = pd.to_numeric(df.get('longitud_caparazon_mm', 0), errors='coerce').fillna(0)
    df['longitud_rostro_mm'] = pd.to_numeric(df.get('longitud_rostro_mm', 0), errors='coerce').fillna(0)
    df['longitud_quela_mm'] = pd.to_numeric(df.get('longitud_quela_mm', 0), errors='coerce').fillna(0)
    df['ancho_quela_mm'] = pd.to_numeric(df.get('ancho_quela_mm', 0), errors='coerce').fillna(0)

    df['ratio_rostro'] = df.apply(
        lambda r: r['longitud_rostro_mm'] / r['longitud_caparazon_mm'] if r['longitud_caparazon_mm'] > 0 else 0, axis=1)
    df['ratio_quela'] = df.apply(
        lambda r: r['longitud_quela_mm'] / r['ancho_quela_mm'] if r['ancho_quela_mm'] > 0 else 0, axis=1)
    return df
