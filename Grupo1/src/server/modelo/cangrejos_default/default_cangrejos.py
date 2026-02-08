
from data.Corutine_training_sync.courutine_training import start_training_thread

#funcion para retornar el csv actualizado con los cangrejos por defecto, esta funcion se llama desde el endpoint /cangrejos_default para actualizar el csv con los cangrejos por defecto cada vez que se accede a ese endpoint
def default_cangrejos():
    start_training_thread()
    return {"mensaje":"¡Éxito! CSV actualizado con los cangrejos por defecto."}