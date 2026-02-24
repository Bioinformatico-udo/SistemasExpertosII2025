"""Transformaciones de características para reglas y ML.

Este módulo normaliza y asegura la presencia de las columnas que el
modelo y las reglas esperan. No realiza codificación compleja (one-hot);
solo garantiza tipos y valores por defecto.
"""

import pandas as pd


def preparar_caracteristicas(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara un DataFrame para uso en reglas y entrenamiento.

    Acciones realizadas:
    - Asegura columnas binarias (`pleon_plegado`, `presencia_setas`) y las fuerza a `int`.
    - Normaliza categorías simples (`ornamentacion_caparazon`, `forma_quela`).
    - Garantiza que los ratios `ratio_rostro` y `ratio_quela` existan.

    Args:
        df: DataFrame con columnas de entrada (puede estar incompleto).

    Returns:
        Copia del DataFrame con columnas limpias y valores por defecto.
    """
    df = df.copy()

    if 'pleon_plegado' in df.columns:
        df['pleon_plegado'] = df['pleon_plegado'].fillna(0).astype(int)
    else:
        df['pleon_plegado'] = 0

    if 'presencia_setas' in df.columns:
        df['presencia_setas'] = df['presencia_setas'].fillna(0).astype(int)
    else:
        df['presencia_setas'] = 0

    df['ornamentacion_caparazon'] = df.get('ornamentacion_caparazon', 'unknown').fillna('unknown')
    df['forma_quela'] = df.get('forma_quela', 'unknown').fillna('unknown')

    # Codificación para ML (IA)
    # ornamentacion: lisa=0, rugosa=1
    df['orn_numeric'] = df['ornamentacion_caparazon'].apply(
        lambda x: 1 if str(x).lower() == 'rugosa' else 0
    )
    # forma_quela: robusta=0, delgada=1
    df['forma_numeric'] = df['forma_quela'].apply(
        lambda x: 1 if str(x).lower() == 'delgada' else 0
    )

    df['ratio_rostro'] = df.get('ratio_rostro', 0).fillna(0)
    df['ratio_quela'] = df.get('ratio_quela', 0).fillna(0)

    return df
