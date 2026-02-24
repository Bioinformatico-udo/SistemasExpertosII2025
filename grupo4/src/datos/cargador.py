"""Funciones para cargar y guardar datos (versión en español).

Este módulo provee utilidades ligeras para trabajar con los CSV de entrada
y salida del proyecto. Está pensado para ser simple y fácil de entender:

- `cargar_csv`: carga el CSV fuente (plantilla o crudo) y devuelve un DataFrame.
- `guardar_csv`: guarda un DataFrame en `data/processed` por defecto.

No realiza transformaciones complejas: esas las realiza `src.datos.preprocesar`
y `src.caracteristicas`.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from ..configuracion import RAW_DATA_DIR


def cargar_csv(path: Optional[str] = None) -> pd.DataFrame:
    """Carga un CSV de registros KommonCats y devuelve un DataFrame.

    Args:
        path: Ruta al CSV. Si es `None`, se usa
            `RAW_DATA_DIR/porcellanids_template.csv`.

    Returns:
        pd.DataFrame con los registros leídos.

    Raises:
        FileNotFoundError: si el fichero no existe.

    Ejemplo:
        >>> df = cargar_csv()
    """
    csv_path = Path(path) if path else Path(RAW_DATA_DIR) / 'porcellanids_template.csv'
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado en {csv_path}")
    df = pd.read_csv(csv_path)
    return df


def guardar_csv(df: pd.DataFrame, out_path: Optional[str] = None) -> str:
    """Guarda un DataFrame en CSV en `data/processed`.

    Si `out_path` no se pasa, se guarda en
    `RAW_DATA_DIR/../processed/porcellanids_processed.csv`.

    Args:
        df: DataFrame a guardar.
        out_path: Ruta opcional de salida.

    Returns:
        Ruta completa del archivo guardado.
    """
    out = Path(out_path) if out_path else Path(RAW_DATA_DIR).parents[0] / 'processed' / 'porcellanids_processed.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return str(out)
