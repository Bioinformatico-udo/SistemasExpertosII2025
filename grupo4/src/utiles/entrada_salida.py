"""Utilidades de lectura/escritura y versionado simple (CSV/Parquet) """

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

def guardar_decision_csv(id_registro: str, decision: dict, out_csv: str):
    """Registra una decisión en un CSV acumulativo.

    Args:
        id_registro: Identificador del registro evaluado.
        decision: Diccionario con la estructura de la decisión (p. ej. reglas/ML).
        out_csv: Ruta al fichero CSV donde guardar el historial.

    Comportamiento:
        - Si `out_csv` existe, añade una fila al final; si no, crea uno nuevo.
        - El campo `decision` se serializa como JSON (utf-8 / sin escape de unicode).
    """
    out_path = Path(out_csv)
    row = {
        'id_registro': id_registro,
        'timestamp': datetime.utcnow().isoformat(),
        'decision': json.dumps(decision, ensure_ascii=False)
    }
    if out_path.exists():
        df = pd.read_csv(out_path)
        df = df.append(row, ignore_index=True)
    else:
        df = pd.DataFrame([row])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

def guardar_snapshot_parquet(df: pd.DataFrame, out_dir: str, prefix: str = 'porcellanids_processed'):
    """Guarda una instantánea del DataFrame en formato Parquet con timestamp.

    Args:
        df: DataFrame a guardar.
        out_dir: Carpeta donde dejar el fichero Parquet.
        prefix: Prefijo del nombre del fichero (por defecto 'porcellanids_processed').

    Returns:
        Ruta al fichero Parquet generado como string.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = out_dir / f"{prefix}_v{ts}.parquet"
    df.to_parquet(out_path, index=False)
    return str(out_path)
