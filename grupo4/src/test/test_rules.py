"""Pruebas unitarias básicas para motor de reglas."""

from src.motor_reglas.reglas import regla_pisidia_brasiliensis
from src.motor_reglas.motor import evaluar_reglas

def test_regla_pisidia_brasiliensis():
    regla = regla_pisidia_brasiliensis()
    # Pisidia: ratio_rostro ~0.26, ratio_quela ~2.25, smooth, robust
    record = {
        'ratio_rostro': 0.26, 
        'ratio_quela': 2.25, 
        'ornamentacion_caparazon': 'smooth',
        'forma_quela': 'robust'
    }
    candidatos = evaluar_reglas(record, [regla])
    assert len(candidatos) == 1
    assert candidatos[0]['species'] == 'Pisidia brasiliensis'
