import streamlit as st
import copy
from base_de_conocimiento import BASE_DE_CONOCIMIENTO
from editar_kb import interfaz_crear_pregunta
from sistema_experto import mostrar_sistema_experto
from portfolio import mostrar_portafolio
from inicio import mostrar_inicio

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
        interfaz_crear_pregunta()

if __name__ == "__main__":
    main()
