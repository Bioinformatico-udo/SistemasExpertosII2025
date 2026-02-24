"""
Generador de Datos Sintéticos para Porcelánidos de Venezuela 🦀📊

Este script es responsable de la técnica de "Data Augmentation" (Aumento de Datos).
Su objetivo es tomar las pocas muestras reales (promedios por especie) y crear
múltiples variaciones simuladas para entrenar al modelo de Inteligencia Artificial.

¿Cómo funciona?
1. Lee el archivo "maestro" con los datos promedio de cada especie (`especies_venezuela.csv`).
2. Para cada especie, genera 50 "clones" virtuales.
3. A cada clon le aplica una pequeña variación aleatoria (ruido) en sus medidas:
   - Longitud de caparazón, rostro, quela, etc.
   - Ejemplo: Si el promedio es 10mm, un clon puede medir 10.2mm, otro 9.8mm.
4. Mantiene los rasgos categóricos (color, forma) intactos o con mínima variación lógica
   (aunque en esta versión se mantienen fijos para garantizar consistencia biológica).
5. Guarda el resultado en `porcellanids_processed.csv`, que será usado para entrenar el modelo.

"""

import pandas as pd
import numpy as np
from pathlib import Path
from src.configuracion import RAW_DATA_DIR, DATA_DIR

def generar_datos_sinteticos(n_samples=50, ruido=0.10):
    """Genera registros sintéticos basados en el CSV maestro.

    Args:
        n_samples: Cuántos clones generar por cada especie original.
        ruido: Factor de variación (0.10 = 10% de desviación estándar).
    """
    ref_path = Path(RAW_DATA_DIR) / 'especies_venezuela.csv'
    output_path = Path(DATA_DIR) / 'porcellanids_processed.csv'

    if not ref_path.exists():
        print(f"Error: No se encuentra el archivo maestro en {ref_path}")
        return

    # 1. Cargar datos de referencia
    df_ref = pd.read_csv(ref_path)
    print(f"Leyendo datos maestros de: {ref_path}")

    columnas_numericas = [
        'longitud_caparazon_mm', 
        'longitud_rostro_mm', 
        'longitud_quela_mm', 
        'ancho_quela_mm'
    ]

    print(f"Generando {n_samples} muestras sinteticas por cada una de las {len(df_ref)} especies...")

    nuevos_registros = []

    # 2. Bucle principal: Para cada especie original...
    for _, row in df_ref.iterrows():
        # Generar N clones
        for _ in range(n_samples):
            nuevo_reg = row.to_dict()
            
            # Aplicar ruido a cada medida numérica
            for col in columnas_numericas:
                valor_base = float(row[col])
                # Variación aleatoria normal
                variacion = np.random.normal(0, valor_base * (ruido/2))
                nuevo_reg[col] = max(0.1, round(valor_base + variacion, 2))
            
            nuevos_registros.append(nuevo_reg)

    # 3. Guardar resultados
    df_sintetico = pd.DataFrame(nuevos_registros)
    
    # Intentamos cargar datos previos si existen para no perderlos
    if output_path.exists():
        print(f"Cargando dataset base para filtrar: {output_path}")
        df_old = pd.read_csv(output_path)
        # Aquí podríamos concatenar o simplemente sobrescribir si queremos un reset
        # Para este proyecto, sobrescribiremos para asegurar limpieza de 11 especies
    
    df_final = df_sintetico
    
    # Crear directorio si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_final.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Dataset final generado con {len(df_final)} registros.")
    print(f"Guardado exitosamente en: {output_path}")

if __name__ == "__main__":
    # Asegurar reproducibilidad
    np.random.seed(42)
    generar_datos_sinteticos()
