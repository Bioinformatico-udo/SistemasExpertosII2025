"""Envoltorio para DecisionTreeClassifier (versión en español).

Clase renombrada a `ModeloML`.
"""

import joblib
from sklearn.tree import DecisionTreeClassifier
from typing import Optional
import numpy as np

class ModeloML:
    """Envoltorio sencillo para `DecisionTreeClassifier`.

    Proporciona métodos convenientes para entrenar, guardar y cargar el
    estimador usado como fallback en la interfaz. Mantiene solo la mínima
    funcionalidad necesaria para este proyecto.

    Métodos principales:
    - `train(X, y, max_depth)`: entrena y guarda en memoria el estimador.
    - `predict(X)`, `predict_proba(X)`: usan el estimador entrenado.
    - `save(path)`, `load(path)`: persistencia con `joblib`.
    - `clases()`: lista de clases aprendidas.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        if model_path:
            self.load(model_path)

    def train(self, X, y, max_depth: int = 5):
        """Entrena un Decision Tree con los datos dados.

        Args:
            X: matriz de características (DataFrame o array-like).
            y: vector objetivo.
            max_depth: profundidad máxima del árbol.

        Returns:
            El estimador ajustado (instancia de DecisionTreeClassifier).
        """
        clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        clf.fit(X, y)
        self.model = clf
        return clf

    def predict_proba(self, X):
        """Devuelve las probabilidades por clase para las muestras en `X`.

        Lanza `ValueError` si el modelo no está entrenado o cargado.
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        return self.model.predict_proba(X)

    def predict(self, X):
        """Predice la clase más probable para las muestras en `X`.

        Lanza `ValueError` si el modelo no está entrenado o cargado.
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        return self.model.predict(X)

    def save(self, path: str):
        """Guarda el estimador en disco usando `joblib`.

        Args:
            path: ruta de salida para el fichero .joblib
        """
        joblib.dump(self.model, path)
        self.model_path = path

    def load(self, path: str):
        """Carga un estimador guardado en `path`.

        Args:
            path: ruta del fichero .joblib a cargar.
        """
        self.model = joblib.load(path)
        self.model_path = path

    def clases(self):
        """Devuelve la lista de clases conocida por el modelo.

        Retorna lista vacía si no hay modelo cargado.
        """
        if self.model is None:
            return []
        return list(self.model.classes_)
