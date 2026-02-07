"""Funciones para cargar CSV e imágenes (validación básica)."""

import pandas as pd
from pathlib import Path
from typing import Optional
from ..config import RAW_DATA_DIR

def cargar_csv(path: Optional[str] = None) -> pd.DataFrame:
    """Carga un CSV de registros KommonCats y devuelve un DataFrame.

    Args:
        path: ruta al CSV. Si None, usa RAW_DATA_DIR/porcellanids_template.csv.

    Returns:
        pd.DataFrame con los registros.
    """
    csv_path = Path(path) if path else Path(RAW_DATA_DIR) / 'porcellanids_template.csv'
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado en {csv_path}")
    df = pd.read_csv(csv_path)
    return df

def guardar_csv(df: pd.DataFrame, out_path: Optional[str] = None) -> str:
    """Guarda DataFrame en CSV en data/processed (crea carpeta si no existe).

    Args:
        df: DataFrame a guardar.
        out_path: ruta de salida opcional.

    Returns:
        Ruta del archivo guardado.
    """
    out = Path(out_path) if out_path else Path(RAW_DATA_DIR).parents[0] / 'processed' / 'porcellanids_processed.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return str(out)

def validar_rutas_imagenes(df: pd.DataFrame, image_dir: Optional[str] = None) -> pd.DataFrame:
    """Verifica que las rutas de imágenes existan; añade columnas 'photo_dorsal_exists' y 'photo_lateral_exists'.

    Args:
        df: DataFrame con columnas 'photo_dorsal' y 'photo_lateral'.
        image_dir: carpeta base de imágenes (si None usa RAW_DATA_DIR/images).

    Returns:
        DataFrame con columnas booleanas indicando existencia de archivos.
    """
    base = Path(image_dir) if image_dir else Path(RAW_DATA_DIR) / 'images'
    df = df.copy()
    df['photo_dorsal_exists'] = df['photo_dorsal'].apply(lambda p: (base / Path(p).name).exists())
    df['photo_lateral_exists'] = df['photo_lateral'].apply(lambda p: (base / Path(p).name).exists())
    return df
