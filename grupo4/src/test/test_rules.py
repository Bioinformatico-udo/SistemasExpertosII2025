"""Pruebas unitarias básicas para motor de reglas."""

from src.rules_engine.rules import regla_porcellana_A
from src.rules_engine.engine import evaluar_reglas

def test_regla_porcellana_A():
    regla = regla_porcellana_A()
    record = {'rostro_ratio': 0.35, 'chela_shape': 'slender', 'pleon_folded': 1}
    candidatos = evaluar_reglas(record, [regla])
    assert len(candidatos) == 1
    assert candidatos[0]['species'] == 'Porcellana sp. A'
