import json

from data.Corutine_training_sync.courutine_training import start_training_thread

def delete_cangrejo(file_path, nombre_especie):
    try:
        with open(file_path,'r+',encoding='utf-8') as f:
            data = json.load(f)
            
            if nombre_especie in data:
                del data[nombre_especie]
                f.seek(0)
                json.dump(data,f,indent = 4)
                f.truncate()
                start_training_thread()
                return {"mensaje": "Especie eliminada exitosamente", "especie": nombre_especie}
            else:
                return {"error": "No se encontro la especie"}
    except Exception:
        return {"error": "Error al eliminar la especie"}
        