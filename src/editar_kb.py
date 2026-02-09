import streamlit as st
import copy
from base_de_conocimiento import BASE_DE_CONOCIMIENTO

def interfaz_crear_pregunta():
    """
    Interfaz para crear preguntas dinámicas en el sistema experto HippoCaribe,
    usando la base de conocimiento existente en st.session_state.kb_dinamica.
    """

    # Inicializar KB dinámica si no existe
    if "kb_dinamica" not in st.session_state:
        st.session_state.kb_dinamica = copy.deepcopy(BASE_DE_CONOCIMIENTO)

    if "nueva_pregunta" not in st.session_state:
        st.session_state.nueva_pregunta = {"texto": "", "nota": "", "imagen": "", "opciones": []}

    st.title("Editor de Preguntas Taxonómicas")

    # Función para recorrer KB y obtener todas las preguntas existentes
    def obtener_preguntas(kb, path=[]):
        preguntas = []
        if "pregunta" in kb:
            preguntas.append({"texto": kb["pregunta"], "path": path.copy(), "kb": kb})
        if "opciones" in kb:
            for opcion, subkb in kb["opciones"].items():
                preguntas.extend(obtener_preguntas(subkb, path + [kb]))
        return preguntas

    preguntas_existentes = obtener_preguntas(st.session_state.kb_dinamica)
    padres = ["-- Ninguna (pregunta raíz) --"] + [p["texto"] for p in preguntas_existentes]
    padre_seleccionado = st.selectbox("Selecciona la pregunta padre", padres)

    # Formulario de nueva pregunta
    st.subheader("Crear nueva pregunta")
    st.session_state.nueva_pregunta["texto"] = st.text_input(
        "Texto de la pregunta", st.session_state.nueva_pregunta["texto"]
    )
    st.session_state.nueva_pregunta["nota"] = st.text_area(
        "Nota (opcional)", st.session_state.nueva_pregunta["nota"]
    )
    st.session_state.nueva_pregunta["imagen"] = st.text_input(
        "URL o path de la imagen (opcional)", st.session_state.nueva_pregunta["imagen"]
    )

    # Agregar opciones a la pregunta
    st.write("Opciones de respuesta")
    for i, opcion in enumerate(st.session_state.nueva_pregunta["opciones"]):
        opcion_texto = st.text_input(f"Opción {i+1}", value=opcion, key=f"opcion_{i}")
        st.session_state.nueva_pregunta["opciones"][i] = opcion_texto

    if st.button("Añadir opción"):
        st.session_state.nueva_pregunta["opciones"].append("")

    # Guardar la pregunta en la KB dinámica
    def guardar_pregunta():
        nueva = st.session_state.nueva_pregunta.copy()
        st.session_state.nueva_pregunta = {"texto": "", "nota": "", "imagen": "", "opciones": []}

        # Convertir opciones a diccionario vacío
        opciones_dic = {op: {} for op in nueva["opciones"]}

        if padre_seleccionado == "-- Ninguna (pregunta raíz) --":
            # Añadir como nuevo nodo raíz sin borrar la KB existente
            if "opciones" not in st.session_state.kb_dinamica:
                st.session_state.kb_dinamica["opciones"] = {}
            st.session_state.kb_dinamica["opciones"][nueva["texto"]] = {
                "nota": nueva.get("nota", ""),
                "imagen": nueva.get("imagen", ""),
                "pregunta": nueva["texto"],
                "opciones": opciones_dic,
            }
        else:
            # Buscar el nodo padre y añadirle esta pregunta
            def agregar_a_padre(kb):
                if "pregunta" in kb and kb["pregunta"] == padre_seleccionado:
                    if "opciones" not in kb:
                        kb["opciones"] = {}
                    # Añadir opciones nuevas sin sobrescribir existentes
                    for op in nueva["opciones"]:
                        if op not in kb["opciones"]:
                            kb["opciones"][op] = {}
                    # Actualizar nota e imagen si están vacías
                    if nueva.get("nota"):
                        kb["nota"] = nueva["nota"]
                    if nueva.get("imagen"):
                        kb["imagen"] = nueva["imagen"]
                    return True
                elif "opciones" in kb:
                    for subkb in kb["opciones"].values():
                        if agregar_a_padre(subkb):
                            return True
                return False

            agregar_a_padre(st.session_state.kb_dinamica)

    st.button("Guardar pregunta", on_click=guardar_pregunta)

    # Mostrar árbol actual
    st.subheader("Preguntas existentes")
    def mostrar_arbol(kb, nivel=0):
        st.json(st.session_state.kb_dinamica)
        if "pregunta" in kb:
            st.markdown("  " * nivel + f"- **{kb['pregunta']}**")
        if "opciones" in kb:
            for opcion, subkb in kb["opciones"].items():
                st.markdown("  " * (nivel + 1) + f"> Opción: {opcion}")
                mostrar_arbol(subkb, nivel + 2)

    mostrar_arbol(st.session_state.kb_dinamica)
