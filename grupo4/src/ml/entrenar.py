"""Script de entrenamiento básico para el Decision Tree (en español)."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from .modelo import ModeloML
from ..datos.preprocesar import calcular_ratios
from ..caracteristicas.ingenieria import preparar_caracteristicas
from ..configuracion import MODEL_PATH
import os

def entrenar_modelo(csv_path: str, target_col: str = 'especie_validada', max_depth: int = 5):
    """Entrena un `DecisionTreeClassifier` sobre un CSV procesado y lo guarda.

    Args:
        csv_path: Ruta al CSV con los registros ya procesados.
        target_col: Nombre de la columna objetivo (por defecto `especie_validada`).
        max_depth: Profundidad máxima para el árbol.

    Raises:
        FileNotFoundError: si `csv_path` no existe.
        ValueError: si hay menos de 2 clases en la columna objetivo.

    Salida:
        Imprime el `classification_report` y guarda el modelo en la ruta
        especificada por la configuración del proyecto.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    df = calcular_ratios(df)
    df = preparar_caracteristicas(df)

    # Definimos el nuevo conjunto de características sincronizado con las reglas
    features = [
        'ratio_rostro', 
        'ratio_quela', 
        'longitud_caparazon_mm',
        'pleon_plegado', 
        'presencia_setas',
        'orn_numeric',
        'forma_numeric'
    ]
    for f in features:
        if f not in df.columns:
            df[f] = 0

    X = df[features]
    y = df[target_col]

    mask = y.notna()
    X = X[mask]
    y = y[mask]

    if len(y.unique()) < 2:
        raise ValueError("Se requieren al menos 2 clases para entrenar el modelo.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    ml = ModeloML()
    ml.train(X_train, y_train, max_depth=max_depth)
    y_pred = ml.predict(X_test)
    print("Reporte de clasificación:\n")
    print(classification_report(y_test, y_pred))
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    ml.save(MODEL_PATH)
    print(f"Modelo guardado en {MODEL_PATH}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python -m src.ml.entrenar path/a/tu/csv.csv [max_depth]")
    else:
        csv = sys.argv[1]
        depth = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        entrenar_modelo(csv, max_depth=depth)
