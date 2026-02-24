r"""Configuración global del proyecto (lectura de `.env`) 

Este módulo centraliza rutas y parámetros configurables del proyecto. Lee
variables de entorno desde un archivo `.env` en la raíz del repositorio y
proporciona valores por defecto útiles para el desarrollo local.

Variables de entorno relevantes (y sus valores por defecto):

- `DATA_DIR`: Carpeta donde se guardan los datos procesados.
	- Por defecto: `<ROOT>/data/processed`
- `RAW_DATA_DIR`: Carpeta con datos crudos y plantillas.
	- Por defecto: `<ROOT>/data/raw`
- `MODEL_PATH`: Ruta al fichero del modelo persistido (`.joblib`).
	- Por defecto: `<ROOT>/models/decision_tree.joblib`
- `LOG_LEVEL`: Nivel de logging (por defecto `INFO`).
- `ENV`: Entorno (`development` por defecto).
- `SECRET_KEY`: llave de uso interno (valor por defecto no seguro).

Notas:
- Estos valores son pensados para desarrollo. En despliegues o CI se
	recomienda definir las variables de entorno apropiadas y no usar los
	valores por defecto.
- Mantén un `.env` en la raíz para personalizar rutas sin editar el código.

Ejemplo mínimo de `.env`:

		DATA_DIR=C:\ruta\a\tu\repo\data\processed
		RAW_DATA_DIR=C:\ruta\a\tu\repo\data\raw
		MODEL_PATH=C:\ruta\a\tu\repo\models\decision_tree.joblib

"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Directorio raíz del proyecto (dos niveles arriba de este archivo)
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / '.env')

# Rutas (archivos y carpetas) — leerán de las variables de entorno o usan
# valores por defecto relativos a la raíz del proyecto.
DATA_DIR = os.getenv('DATA_DIR', str(ROOT / 'data' / 'processed'))
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR', str(ROOT / 'data' / 'raw'))
MODEL_PATH = os.getenv('MODEL_PATH', str(ROOT / 'models' / 'decision_tree.joblib'))

# Parámetros generales
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENV = os.getenv('ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'valor_por_defecto_no_seguro')

# Helper: ruta al proyecto para uso en logs y UIs
PROJECT_ROOT = ROOT
