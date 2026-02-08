

from data.sync_csv_json.sync_csv import sync_csv_json

#funcion para retornar el csv actualizado con los cangrejos por defecto, esta funcion se llama desde el endpoint /cangrejos_default para actualizar el csv con los cangrejos por defecto cada vez que se accede a ese endpoint
def default_cangrejos():
    sync_csv_json('modelo/cangrejos_default/default_cangrejos.json')
    return {"mensaje":"¡Éxito! CSV actualizado con los cangrejos por defecto."}