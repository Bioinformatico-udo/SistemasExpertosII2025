"""Tests para el encadenamiento hacia atrás (backward chaining)."""

import pytest
from src.motor_reglas.motor import verificar_especie, buscar_regla_por_especie
from src.motor_reglas.reglas import reglas_iniciales


def test_buscar_regla_existente():
    """Verifica que se puede encontrar una regla por nombre de especie."""
    reglas = reglas_iniciales()
    regla = buscar_regla_por_especie('Porcellana sp. A', reglas)
    
    assert regla is not None
    assert regla['species'] == 'Porcellana sp. A'
    assert regla['id'] == 'R_PORC_A'


def test_buscar_regla_inexistente():
    """Verifica que devuelve None cuando la especie no existe."""
    reglas = reglas_iniciales()
    regla = buscar_regla_por_especie('Especie Inexistente', reglas)
    
    assert regla is None


def test_buscar_regla_case_insensitive():
    """Verifica que la búsqueda es case-insensitive."""
    reglas = reglas_iniciales()
    regla = buscar_regla_por_especie('porcellana sp. a', reglas)
    
    assert regla is not None
    assert regla['species'] == 'Porcellana sp. A'


def test_verificar_especie_exitosa():
    """Verifica que backward chaining confirma especie cuando se cumplen condiciones."""
    reglas = reglas_iniciales()
    
    # Record que cumple todas las condiciones de Porcellana sp. A
    record = {
        'ratio_rostro': 0.35,
        'forma_quela': 'slender',
        'pleon_plegado': 1
    }
    
    resultado = verificar_especie(record, 'Porcellana sp. A', reglas)
    
    assert resultado['verificada'] is True
    assert resultado['score'] == 1.0
    assert resultado['condiciones_cumplidas'] == 3
    assert resultado['condiciones_faltantes'] == 0
    assert resultado['regla_encontrada'] is True


def test_verificar_especie_fallida():
    """Verifica que backward chaining rechaza especie cuando no se cumplen condiciones."""
    reglas = reglas_iniciales()
    
    # Record que NO cumple las condiciones de Porcellana sp. A
    record = {
        'ratio_rostro': 0.20,  # Muy bajo (< 0.30)
        'forma_quela': 'robust',  # No coincide
        'pleon_plegado': 0  # No coincide
    }
    
    resultado = verificar_especie(record, 'Porcellana sp. A', reglas)
    
    assert resultado['verificada'] is False
    assert resultado['score'] == 0.0
    assert resultado['condiciones_cumplidas'] == 0
    assert resultado['condiciones_faltantes'] == 3
    assert resultado['regla_encontrada'] is True


def test_verificar_especie_parcial():
    """Verifica comportamiento cuando se cumplen algunas condiciones pero no todas."""
    reglas = reglas_iniciales()
    
    # Record que cumple solo 2 de 3 condiciones
    record = {
        'ratio_rostro': 0.35,  # ✓
        'forma_quela': 'slender',  # ✓
        'pleon_plegado': 0  # ✗
    }
    
    resultado = verificar_especie(record, 'Porcellana sp. A', reglas)
    
    # Score: 2/3 = 0.67, threshold = 0.66, debería pasar
    assert resultado['verificada'] is True
    assert resultado['score'] == 0.67
    assert resultado['condiciones_cumplidas'] == 2
    assert resultado['condiciones_faltantes'] == 1


def test_verificar_especie_inexistente():
    """Verifica comportamiento cuando se busca una especie sin regla definida."""
    reglas = reglas_iniciales()
    
    record = {'ratio_rostro': 0.35}
    resultado = verificar_especie(record, 'Especie Ficticia', reglas)
    
    assert resultado['verificada'] is False
    assert resultado['regla_encontrada'] is False
    assert 'No existe una regla definida' in resultado['mensaje']


def test_verificar_petrolisthes():
    """Verifica que funciona correctamente con Petrolisthes sp. B."""
    reglas = reglas_iniciales()
    
    # Record que cumple condiciones de Petrolisthes
    record = {
        'ornamentacion_caparazon': 'smooth',
        'forma_quela': 'robust',
        'espinas_rostro_count': 0
    }
    
    resultado = verificar_especie(record, 'Petrolisthes sp. B', reglas)
    
    assert resultado['verificada'] is True
    assert resultado['score'] == 1.0
    assert resultado['especie'] == 'Petrolisthes sp. B'


def test_resultado_contiene_mensaje_explicativo():
    """Verifica que el resultado incluye mensajes explicativos claros."""
    reglas = reglas_iniciales()
    
    record = {
        'ratio_rostro': 0.35,
        'forma_quela': 'slender',
        'pleon_plegado': 1
    }
    
    resultado = verificar_especie(record, 'Porcellana sp. A', reglas)
    
    assert 'mensaje' in resultado
    assert 'Porcellana sp. A' in resultado['mensaje']
    assert 'threshold' in resultado['mensaje'].lower()
