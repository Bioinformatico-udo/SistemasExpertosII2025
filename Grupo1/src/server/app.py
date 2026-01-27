from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from constantes.preguntas import PREGUNTAS
from modelo.prueba_tensorflow import modelo_cangrejo
from flask_cors import CORS

app = Flask(__name__)
#secret key para la sesion y el guardado de la informacion
app.secret_key = '1234566789'
CORS(app)



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




if __name__ == '__main__':
    app.run(debug=True)