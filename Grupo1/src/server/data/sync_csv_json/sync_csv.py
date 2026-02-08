import pandas as pd
import json
#funcion para guardas los datos de las preguntas del json en el csv para el entrenamiento del modelo
def sync_csv_json(ruta_json):
    with open(ruta_json, 'r',encoding='utf-8') as f:
        data_json = json.load(f)
    columnnas_caracteristicas = ['superficie_lisa','superficie_irregular','antena_lisa','antena_aserrado','maxilipedos_lisos','maxilipedos_con_surcos','quelipedos_desiguales','quelipedos_iguales','caparazon_cuadrado','caparazon_rectangular','telson_siete','telson_cinco','si_pleopodo','no_pleopodo','habitats_protegidos','habitats_expuestos']
    columnafinal = ['Especie'] + columnnas_caracteristicas
    filas = []
    
    for especie, detalles in data_json.items():
        if 'preguntas_identificacion' in detalles:
            fila = [especie] + detalles['preguntas_identificacion']
            filas.append(fila)
        else:
            print(f"Advertencia: La especie '{especie}' no tiene 'preguntas_identificacion' en el JSON.")
    
    df = pd.DataFrame(filas, columns=columnafinal)
    df.to_csv('modelo/cangrejos.csv', index=False)
    print(f"¡Éxito! CSV actualizado con {len(filas)} especies.")

sync_csv_json('data/Cangrejos.json')