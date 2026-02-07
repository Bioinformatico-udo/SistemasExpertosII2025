"""Prueba mínima para wrapper ML (sin entrenamiento real)."""

from src.ml.model import MLModel
import pandas as pd
import numpy as np

def test_ml_wrapper_save_load(tmp_path):
    X = pd.DataFrame(np.random.rand(10,3), columns=['a','b','c'])
    y = ['s1']*5 + ['s2']*5
    ml = MLModel()
    ml.train(X, y, max_depth=2)
    path = tmp_path / "model.joblib"
    ml.save(str(path))
    ml2 = MLModel()
    ml2.load(str(path))
    assert ml2.model is not None
