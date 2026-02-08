import threading
from modelo.prueba_tensorflow import entrenar_modelo_cangrejo
from data.sync_csv_json.sync_csv import sync_csv_json

training_thread = None

#funcion para ser llamada en segundo plano para entrenar el modelo sin bloquear la ejecucion del servidor, se llama cada vez que se actualiza o elimina una especie para mantener el modelo actualizado con los nuevos datos
def training_coroutine():
    print("Iniciando entrenamiento del modelo...")
    sync_csv_json()
    entrenar_modelo_cangrejo()    
    print("Entrenamiento del modelo completado.")
    
def start_training_thread():
    #se declara la variable global para el hilo de entrenamiento
    global training_thread
    #si el hilo de entrenamiento ya esta en progreso, no se inicia otro para evitar conflictos
    if training_thread is not None and training_thread.is_alive():
        print("El entrenamiento ya está en progreso. Por favor, espera a que termine.")
        return
    #funcion para iniciar el hilo de entrenamiento
    training_thread = threading.Thread(target=training_coroutine)
    training_thread.start()
    