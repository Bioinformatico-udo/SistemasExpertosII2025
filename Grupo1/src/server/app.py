import json
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from constantes.preguntas import PREGUNTAS
from modelo.prueba_tensorflow import modelo_cangrejo
from flask_cors import CORS
from data.read_json_cangrejos.read_cangrejos import read_cangrejos

app = Flask(__name__)
#secret key para la sesion y el guardado de la informacion
app.secret_key = '1234566789'
CORS(app)
file_path_json = 'data/Cangrejos.json'



@app.route('/cangrejos', methods=['POST'])
def cangrejos():
    if request.is_json:
        try:
            data = request.get_json()
            arrayToModel = data.get('elementos')
            cangrejo_encontrado = modelo_cangrejo(arrayToModel)

            return jsonify({"mensaje": "Array procesado",
                        "cangrejo":cangrejo_encontrado}),200
        except Exception:
            return jsonify({"error":"error en json"}),500
    else:
        return jsonify({"error":"error al detectar"}),400

@app.route('/catalogo', methods=['GET'])
def catalogo():
    try:
        return read_cangrejos(file_path_json)
    except Exception:
        return jsonify({"error":"error al cargar catalogo"}),500

@app.route('/guardar_especimen', methods=['POST'])
def guardar_especimen():
    pass

@app.route('/borrar_especimen/<nombre_especie>', methods=['DELETE'])
def borrar_especimen(nombre_especie):
    pass

if __name__ == '__main__':
    app.run(debug=True)