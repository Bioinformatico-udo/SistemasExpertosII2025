"""Paquete `src.motor_reglas` con reglas y motor."""

from .reglas import reglas_iniciales, obtener_especies_disponibles
from .motor import evaluar_reglas, verificar_especie, buscar_regla_por_especie

__all__ = ['reglas_iniciales', 'obtener_especies_disponibles', 'evaluar_reglas', 'verificar_especie', 'buscar_regla_por_especie']
