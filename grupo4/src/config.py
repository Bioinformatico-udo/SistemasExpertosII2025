"""Configuración global del proyecto (leer .env)."""

from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar .env desde la raíz del proyecto
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / '.env')

# Rutas (archivos y carpetas)
DATA_DIR = os.getenv('DATA_DIR', str(ROOT / 'data' / 'processed'))
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR', str(ROOT / 'data' / 'raw'))
IMAGE_STORAGE_PATH = os.getenv('IMAGE_STORAGE_PATH', str(ROOT / 'data' / 'raw' / 'images'))
MODEL_PATH = os.getenv('MODEL_PATH', str(ROOT / 'models' / 'decision_tree.joblib'))

# Parámetros
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENV = os.getenv('ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'valor_por_defecto_no_seguro')

# Notas:
# - Este archivo no asume una base de datos. Si en el futuro decides usar una,
#   puedes descomentar y configurar DATABASE_URL en .env y añadir la lógica en src/data.
