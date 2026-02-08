import json

def update_cangrejos(file_path,especie_nueva):
    especie_id = especie_nueva['nombreCientifico'].replace(" ", "_")
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            cangrejos = json.load(f)
            cangrejos[especie_id] = especie_nueva
            f.seek(0)
            json.dump(cangrejos, f, indent=4, ensure_ascii=False)
            f.truncate()
        return {"mensaje": "Especie guardada exitosamente", "especie": especie_id}
    except Exception:
        return {"error": "Error al guardar la especie"}