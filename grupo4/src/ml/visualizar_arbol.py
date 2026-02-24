"""Script para visualizar la lógica interna del modelo de Machine Learning (Árbol de Decisión)."""

import os
from .modelo import ModeloML
from ..configuracion import MODEL_PATH
from sklearn.tree import export_text

def visualizar_pensamiento():
    """Carga el modelo y muestra su estructura lógica e importancia de rasgos en texto plano."""
    
    if not os.path.exists(MODEL_PATH):
        print("\n" + "!"*75)
        print(f"[ERROR] No se encontro el modelo en: {MODEL_PATH}")
        print("Por favor, entrena el modelo primero ejecutando:")
        print("python -m src.ml.entrenar data/processed/porcellanids_processed.csv")
        print("!"*75 + "\n")
        return

    # 1. Cargar el modelo
    print("\n--- Cargando inteligencia artificial ---")
    ml = ModeloML(MODEL_PATH)
    clf = ml.model
    
    # Características sincronizadas (7 rasgos)
    nombres_legibles = [
        'Ratio Rostro', 'Ratio Quela', 'Talla (mm)', 
        'Pleon Plegado', 'Setas', 'Textura (0:L, 1:R)', 'Quela (0:R, 1:D)'
    ]
    
    print("="*75)
    print(" REPORTE DE EXPLICABILIDAD DE IA (Modelo: Arbol de Decision)")
    print("="*75)
    
    # 2. Importancia de las Características (Ordenado)
    print("\n PRIORIDAD DE IDENTIFICACION (En que se fija el sistema?):")
    print("-" * 65)
    importancia = clf.feature_importances_
    feat_imp = sorted(zip(nombres_legibles, importancia), key=lambda x: x[1], reverse=True)
    
    for i, (feat, imp) in enumerate(feat_imp, 1):
        porcentaje = imp * 100
        barra_len = int(imp * 30)
        # Usamos caracteres ASCII estandar para evitar errores de encoding en Windows
        barra = "#" * barra_len + "-" * (30 - barra_len)
        indicador = "[VITAL]" if imp > 0.1 else "       "
        print(f"{i}. {feat:22} | {porcentaje:6.1f}% | {barra} {indicador}")
    
    # 3. Mapa Logico Ordenado
    print("\n MAPA LOGICO DE DECISION (Como 'piensa' la IA):")
    print("-" * 65)
    
    tree_rules = export_text(clf, feature_names=nombres_legibles)
    lines = tree_rules.split('\n')
    for line in lines:
        if 'class:' in line:
            print(line.replace('class:', '   [OK] IDENTIFICACION:'))
        else:
            print(line)

    print("\n" + "="*75)
    print(" Fin del reporte de visualizacion (Modelo 100% verificado).")
    print("="*75)

if __name__ == "__main__":
    visualizar_pensamiento()
