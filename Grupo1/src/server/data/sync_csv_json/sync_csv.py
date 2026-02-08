import pandas as pd
import json
from modelo.prueba_tensorflow import entrenar_modelo_cangrejo


#funcion para guardas los datos de las preguntas del json en el csv para el entrenamiento del modelo
def sync_csv_json(ruta_json="data/Cangrejos.json"):
    #lee el json
    with open(ruta_json, 'r',encoding='utf-8') as f:
        data_json = json.load(f)
    #crea una lista de las columnas del csv
    columnnas_caracteristicas = ['superficie_lisa','superficie_irregular','antena_lisa','antena_aserrado','maxilipedos_lisos','maxilipedos_con_surcos','quelipedos_desiguales','quelipedos_iguales','caparazon_cuadrado','caparazon_rectangular','telson_siete','telson_cinco','si_pleopodo','no_pleopodo','habitats_protegidos','habitats_expuestos']
    #crea una lista de las filas del csv
    columnafinal = ['Especie'] + columnnas_caracteristicas
    #variable para guardar las filas del csv
    filas = []
    
    for especie, detalles in data_json.items():
        if 'preguntas_identificacion' in detalles:
            fila = [especie] + detalles['preguntas_identificacion']
            filas.append(fila)
        else:
            print(f"Advertencia: La especie '{especie}' no tiene 'preguntas_identificacion' en el JSON.")
    #crea un dataframe con las filas y columnas y lo guarda en un csv
    df = pd.DataFrame(filas, columns=columnafinal)
    df.to_csv('modelo/cangrejos.csv', index=False)
    print(f"¡Éxito! CSV actualizado con {len(filas)} especies.")
    #despues de actualizar el csv, entrena el modelo con los nuevos datos
