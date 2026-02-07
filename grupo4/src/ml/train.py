"""Script de entrenamiento básico para el Decision Tree."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from .model import MLModel
from ..data.preprocess import calcular_ratios
from ..features.engineering import preparar_features
from ..config import MODEL_PATH
import os

def entrenar_modelo(csv_path: str, target_col: str = 'species_validated', max_depth: int = 5):
    """Carga datos, prepara features, entrena y guarda el modelo.

    Args:
        csv_path: ruta al CSV con registros validados.
        target_col: columna objetivo con la etiqueta de especie.
        max_depth: profundidad máxima del árbol.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    df = calcular_ratios(df)
    df = preparar_features(df)

    # Selección de features (ajustar según disponibilidad)
    features = ['rostro_ratio', 'chela_ratio', 'pleon_folded', 'setae_presence']
    for f in features:
        if f not in df.columns:
            df[f] = 0

    X = df[features]
    y = df[target_col]

    # Filtrar registros con etiqueta válida
    mask = y.notna()
    X = X[mask]
    y = y[mask]

    if len(y.unique()) < 2:
        raise ValueError("Se requieren al menos 2 clases para entrenar el modelo.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    ml = MLModel()
    ml.train(X_train, y_train, max_depth=max_depth)
    y_pred = ml.predict(X_test)
    print("Reporte de clasificación:\n")
    print(classification_report(y_test, y_pred))
    # Crear carpeta models si no existe
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    ml.save(MODEL_PATH)
    print(f"Modelo guardado en {MODEL_PATH}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python -m src.ml.train path/a/tu/csv.csv [max_depth]")
    else:
        csv = sys.argv[1]
        depth = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        entrenar_modelo(csv, max_depth=depth)
