"""Utilidades de lectura/escritura y versionado simple (CSV/Parquet)."""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

def guardar_decision_csv(record_id: str, decision: dict, out_csv: str):
    """Añade una fila con la decisión al CSV de decisiones (crea si no existe).

    Args:
        record_id: identificador del registro.
        decision: diccionario con la decisión (species, score, method, justification).
        out_csv: ruta al CSV de salida.
    """
    out_path = Path(out_csv)
    row = {
        'record_id': record_id,
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
    """Guarda snapshot en Parquet con timestamp para auditoría."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = out_dir / f"{prefix}_v{ts}.parquet"
    df.to_parquet(out_path, index=False)
    return str(out_path)
