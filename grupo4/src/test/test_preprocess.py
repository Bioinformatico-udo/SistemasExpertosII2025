"""Pruebas unitarias básicas para preprocesado."""

import pandas as pd
from src.data.preprocess import calcular_ratios

def test_calcular_ratios():
    df = pd.DataFrame([{
        'carapace_length_mm': 10,
        'rostro_length_mm': 3,
        'chela_length_mm': 12,
        'chela_width_mm': 4
    }])
    out = calcular_ratios(df)
    assert out['rostro_ratio'].iloc[0] == 0.3
    assert out['chela_ratio'].iloc[0] == 3.0
