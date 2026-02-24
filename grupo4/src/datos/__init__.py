"""Paquete `src.datos` con módulos en español."""

from .cargador import cargar_csv, guardar_csv, validar_rutas_imagenes
from .preprocesar import calcular_ratios

__all__ = [
    'cargar_csv', 'guardar_csv', 'validar_rutas_imagenes', 'calcular_ratios'
]
