# Porcellanids Expert

**Proyecto:** Sistema experto híbrido para identificar especies de porcelánidos en Venezuela usando la metodología KommonCats.

## Objetivo
Construir una herramienta reproducible que combine un motor de reglas taxonómicas (KommonCats) y un modelo interpretable (Decision Tree) para proponer identidades taxonómicas a partir de caracteres morfológicos y metadatos.

## Estructura del repositorio
- `data/` : datos crudos, intermedios y procesados (CSV/Parquet + imágenes).
- `src/` : código fuente (config, carga, preprocesado, reglas, ML, UI, utilidades).
- `docs/` : metodología, glosario y guía de instalación.
- `tests/` : pruebas unitarias.

## Requisitos
Ver `requirements.txt`.

## Primeros pasos
1. abre la carpeta: Sistema_Experto_Porcelanidos
2. usar Python 3.11; y crear venv:
	# Si instalaste Python 3.11 y quieres un venv nuevo
	py -3.11 -m venv .venv
3. activar el entorno virtual
	.venv\Scripts\Activate.ps1
4. actualizar pip e instalar dependencia 
	py -m pip install --upgrade pip setuptools wheel
	py -m pip install -r requirements.txt
5. verifica que el csv procesado existe y contiene la columna objetivo
	# listar archivos processed
	Get-ChildItem .\data\processed\

	# mostrar columnas y primeras filas
	py -c "import pandas as pd; df=pd.read_csv('data/processed/porcellanids_processed.csv'); print('Columnas:', list(df.columns)); print(df.head().to_string())"
6. si no existe se crea: 
	py -c "import os,pandas as pd; os.makedirs('data/processed',exist_ok=True); df=pd.read_csv('data/raw/porcellanids_template.csv'); df['area']=df.get('ancho',0)*df.get('alto',0); df['grietas_ratio']=df.get('grietas',0)/(df['area']+1e-6); df.fillna(0).to_csv('data/processed/porcellanids_processed.csv',index=False); print('Guardado data/processed/porcellanids_processed.csv')"
7. entrenar modelo 
	py -m src.ml.train data/processed/porcellanids_processed.csv
8. ejecutar la interfaz
	py -m src.ui.app
9. Probar predicción directa con el modelo guardado:
	py -c "import joblib,pandas as pd; m=joblib.load('models/decision_tree.joblib'); df=pd.read_csv('data/processed/porcellanids_processed.csv'); X=df.drop(columns=['record_id','species_validated','species_provisional'],errors='ignore'); print(m.predict(X.head(1))); print(m.predict_proba(X.head(1)))"
10. ejecutar tests:
	py -m pytest -q

extras: 
Get-ChildItem .\data\processed\; permite ver si hay tablas para procesar
Get-ChildItem .\models\; permite ver si hay un modelo entrenado