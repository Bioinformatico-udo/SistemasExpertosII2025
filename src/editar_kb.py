import streamlit as st
from motor_de_inferencia import MotorDeInferencia



def buscar_y_asignar(nodo, opcion, especie):
    if "opciones" in nodo:
        for op, contenido in nodo["opciones"].items():
            if op == opcion:
                contenido["resultado"] = especie
                return True
            if buscar_y_asignar(contenido, opcion, especie):
                return True
    return False


def buscar_y_crear(nodo, opcion_padre, nueva_pregunta, nuevas_opciones):
    if "opciones" in nodo:
        for op, contenido in nodo["opciones"].items():
            if op == opcion_padre:
                contenido["pregunta"] = nueva_pregunta
                contenido["opciones"] = {
                    o.strip(): {} for o in nuevas_opciones.splitlines()
                }
                return True
            if buscar_y_crear(contenido, opcion_padre, nueva_pregunta, nuevas_opciones):
                return True
    return False


def mostrar_editor_kb():
    st.title("Editor de Base de Conocimiento")

    kb = st.session_state.kb_dinamica

    # -------------------------
    # CREAR PREGUNTA RAÍZ
    # -------------------------

    st.subheader("Crear nueva pregunta")

    pregunta = st.text_input("Texto de la pregunta", key="pregunta_root")
    imagen = st.text_input("Ruta de imagen (opcional)", key="imagen_root")

    opciones_raw = st.text_area(
        "Opciones (una por línea)",
        placeholder="Largo\nCorto\nMediano",
        key="opciones_root"
    )

    if st.button("Crear pregunta raíz"):
        opciones = {op.strip(): {} for op in opciones_raw.splitlines() if op.strip()}

        kb.clear()
        kb["pregunta"] = pregunta
        kb["imagen"] = imagen
        kb["opciones"] = opciones

        st.success("Pregunta raíz creada")

    st.divider()

    # -------------------------
    # ASIGNAR ESPECIE
    # -------------------------

    st.subheader("Asignar especie a opción")

    opcion = st.text_input("Nombre exacto de la opción", key="opcion_especie")
    especie = st.text_input("Nombre de la especie", key="especie")

    if st.button("Asignar especie"):
        if buscar_y_asignar(kb, opcion, especie):
            st.success("Especie asignada correctamente")
        else:
            st.error("Opción no encontrada")

    st.divider()

    # -------------------------
    # CREAR SUBPREGUNTA
    # -------------------------

    st.subheader("Convertir opción en nueva pregunta")

    opcion_padre = st.text_input("Opción a convertir", key="opcion_padre")
    nueva_pregunta = st.text_input("Texto de nueva pregunta", key="nueva_pregunta")

    nuevas_opciones = st.text_area(
        "Nuevas opciones (una por línea)",
        key="nuevas_opciones"
    )

    if st.button("Crear subpregunta"):
        if buscar_y_crear(kb, opcion_padre, nueva_pregunta, nuevas_opciones):
            st.success("Subpregunta creada")
        else:
            st.error("Opción no encontrada")