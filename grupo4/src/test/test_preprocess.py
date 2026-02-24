"""Pruebas unitarias básicas para preprocesado."""

import pandas as pd
from src.datos.preprocesar import calcular_ratios

def test_calcular_ratios():
    df = pd.DataFrame([{
        'longitud_caparazon_mm': 10,
        'longitud_rostro_mm': 3,
        'longitud_quela_mm': 12,
        'ancho_quela_mm': 4
    }])
    out = calcular_ratios(df)
    assert out['ratio_rostro'].iloc[0] == 0.3
    assert out['ratio_quela'].iloc[0] == 3.0
