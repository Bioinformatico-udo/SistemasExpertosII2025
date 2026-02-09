import streamlit as st
import copy
from base_de_conocimiento import BASE_DE_CONOCIMIENTO
from editar_kb import mostrar_inicio,mostrar_portafolio,mostrar_sistema_experto,mostrar_editor_kb



if "kb_dinamica" not in st.session_state:
    st.session_state.kb_dinamica = copy.deepcopy(BASE_DE_CONOCIMIENTO)


def main():
    st.set_page_config(page_title="Sistema Experto", layout="centered")

    menu = st.sidebar.radio(
        "Menú",
        ["Inicio", "Identificar especie","Editor KB", "Contacto"]
    )

    if menu == "Identificar especie":
        mostrar_sistema_experto()
    if menu == "Contacto":
        mostrar_portafolio()
    if menu == "Inicio":
        mostrar_inicio()
    if menu == "Editor KB":
        mostrar_editor_kb()





if __name__ == "__main__":
    main()
