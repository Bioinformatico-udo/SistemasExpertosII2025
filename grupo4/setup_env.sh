#!/usr/bin/env bash
# Script para crear entorno virtual e instalar dependencias (Linux/macOS)

set -e

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Entorno creado e dependencias instaladas."
echo "Activa el entorno con: source .venv/bin/activate"
