import streamlit as st
from src.core.sistema_experto import mostrar_sistema_experto

def mostrar_inicio():
    
    st.markdown("""
        
        <style>
        .block-container {
            max-width: 98% !important;
            padding-top: 1.5rem !important;
        }

        .main-header {
            font-size: 5rem;
            font-weight: 800;
            color: #EAECEE;
            line-height: 1;
            margin-bottom: 0.5rem;
        }
        
        .tagline {
            font-size: 1.3rem;
            color: #2874A6; 
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-bottom: 3rem;
        }

        .info-panel {
            background: #0D1117; 
            border-radius: 12px;
            padding: 2.5rem;
            border: 1px solid #30363D;
            height: 100%;
        }
        
        .info-panel h4 {
            color: #5DADE2 !important; 
            font-size: 1.6rem !important;
            margin-bottom: 1rem !important;
        }

        .metric-box {
            background: #161B22;
            padding: 2rem 1rem;
            border-radius: 10px;
            border-bottom: 3px solid #2874A6;
            text-align: center;
        }
        .metric-num {
            font-size: 2.8rem;
            font-weight: 700;
            color: #EAECEE;
        }
        .metric-txt {
            font-size: 0.85rem;
            color: #8B949E;
            text-transform: uppercase;
        }

        div.stButton > button {
            background-color: #2874A6 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 0.8rem 2rem !important;
            font-size: 1.1rem !important;
            border: none !important;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1B4F72 !important;
            border: none !important;
        }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    """, unsafe_allow_html=True) 

    c1, c2 = st.columns([1.5, 1], gap="large")
    with c1:
        st.markdown('<h1 class="main-header">HippoCaribe</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline">Taxonomía Digital Avanzada</p>', unsafe_allow_html=True)
        st.markdown("""
            <div style="font-size: 1.2rem; color: #8B949E; text-align: justify; margin-bottom: 2rem;">
            Plataforma especializada en la determinación taxonómica de la superfamilia <b>Hippoidea</b>. 
            Este sistema experto digitaliza claves morfológicas complejas para asistir en la clasificación 
            precisa de especímenes en el Caribe venezolano mediante un motor de inferencia lógica.
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("IDENTIFICAR ESPECIE", use_container_width=True):
            mostrar_sistema_experto()

    with c2:
        st.image("assets/SE.png", use_container_width=True)

    st.write("---")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-box"><div class="metric-num">07</div><div class="metric-txt">Especies</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-box"><div class="metric-num">58%</div><div class="metric-txt">Diversidad</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-box"><div class="metric-num">02</div><div class="metric-txt">Familias</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-box"><div class="metric-num">v2.0</div><div class="metric-txt">KB Engine</div></div>', unsafe_allow_html=True)

    st.write("---")

    i1, i2 = st.columns(2, gap="medium")
    with i1:
        st.markdown("""
            <div class="info-panel">
                <h4> <i class="fa-solid fa-microscope"></i> Rigor Científico</h4>
                <p style="color: #8B949E;">Base de conocimiento validada con inventarios biológicos regionales:</p>
                <ul style="color: #8B949E;">
                    <li>Análisis de pedúnculos oculares y antenas.</li>
                    <li>Morfología del telson y dáctilos de los pereiópodos.</li>
                    <li>Registros actualizados de costas venezolanas.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with i2:
        st.markdown("""
            <div class="info-panel">
                <h4><i class="fa-solid fa-gear"></i> Motor de Inferencia</h4>
                <p style="color: #8B949E;">Tecnología aplicada para reducir el error humano en laboratorio:</p>
                <ul style="color: #8B949E;">
                    <li>Lógica dicotómica asistida por imagen.</li>
                    <li>Resultados basados en evidencia morfológica.</li>
                    <li>Editor de reglas para actualización de la KB.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
