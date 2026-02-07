"""Wrapper para modelo scikit-learn (DecisionTreeClassifier)."""

import joblib
from sklearn.tree import DecisionTreeClassifier
from typing import Optional
import numpy as np

class MLModel:
    """Clase envoltorio para entrenar, guardar y predecir con DecisionTree."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        if model_path:
            self.load(model_path)

    def train(self, X, y, max_depth: int = 5):
        """Entrena un DecisionTreeClassifier y lo guarda en memoria."""
        clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        clf.fit(X, y)
        self.model = clf
        return clf

    def predict_proba(self, X):
        """Devuelve probabilidades por clase (requiere modelo entrenado)."""
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        return self.model.predict_proba(X)

    def predict(self, X):
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        return self.model.predict(X)

    def save(self, path: str):
        joblib.dump(self.model, path)
        self.model_path = path

    def load(self, path: str):
        self.model = joblib.load(path)
        self.model_path = path

    def clases(self):
        """Devuelve lista de clases del modelo (si está cargado)."""
        if self.model is None:
            return []
        return list(self.model.classes_)
