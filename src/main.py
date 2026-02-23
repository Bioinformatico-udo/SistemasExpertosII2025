import streamlit as st
import copy
from streamlit_option_menu import option_menu
from datetime import datetime

# Imports de módulos
from src.data.base_de_conocimiento import BASE_DE_CONOCIMIENTO
from src.ui.pages.editar_kb import interfaz_crear_pregunta
from src.core.sistema_experto import mostrar_sistema_experto
from src.ui.pages.portfolio import mostrar_portafolio
from src.ui.pages.inicio import mostrar_inicio



def main():
    st.set_page_config(page_title="HippoCaribe", page_icon="🦀", layout="wide")
    anio_actual = datetime.now().year

    if "kb_dinamica" not in st.session_state:
        st.session_state.kb_dinamica = copy.deepcopy(BASE_DE_CONOCIMIENTO)

    st.markdown("""
        <style>
        /* Contenedor universal para centrar elementos en el sidebar */
        .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }

        /* Ajuste de selección de menú */
        .nav-link {
            border-radius: 10px !important;
            margin: 4px 0px !important;
        }

        /* Estilo para el footer anclado al fondo del sidebar */
        .sidebar-footer {
            position: fixed;
            bottom: 20px;
            width: 260px; /* Ajuste aproximado al ancho del sidebar */
            text-align: center;
            color: #808080;
            font-size: 0.75rem;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: st.image("assets/Albuneidae.png", width=150)
        
        st.markdown(f"""
            <div class="sidebar-content">
                <h2 style='color: #FAFAFA; margin-bottom: 0px; text-align: center;'>HippoCaribe</h2>
                <p style='color: #808080; font-size: 0.85rem; text-align: center;'>Taxonomía Digital</p>
            </div>
            <hr style='border-color: #333; margin-top: 10px; margin-bottom: 20px; width: 100%;'>
        """, unsafe_allow_html=True)

        menu = option_menu(
            menu_title=None, 
            options=["Inicio", "Identificar especie", "Editor KB", "Contacto"],
            icons=["house-fill", "search", "pencil-square", "person-vcard-fill"], 
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#FAFAFA", "font-size": "18px"}, 
                "nav-link": {"font-size": "15px", "text-align": "left", "color": "#FAFAFA", "--hover-color": "#1B4F7268"},
                "nav-link-selected": {"background-color": "#1B4F72", "font-weight": "600"},
            }
        )
        
        st.markdown(f"""
            <div class="sidebar-footer">
                © {anio_actual} HippoCaribe<br>
                Sistemas Expertos<br>
                Universidad de Oriente
            </div>
        """, unsafe_allow_html=True)

    if menu == "Inicio":
        mostrar_inicio()
    elif menu == "Identificar especie":
        mostrar_sistema_experto()
    elif menu == "Editor KB":
        interfaz_crear_pregunta()
    elif menu == "Contacto":
        mostrar_portafolio()

if __name__ == "__main__":
    main()