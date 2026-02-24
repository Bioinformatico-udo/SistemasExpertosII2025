import streamlit as st
import base64
import os
import time
from src.core.motor_de_inferencia import MotorDeInferencia

def get_base64_image(image_path):
    """Conversión de activos visuales a base64 para renderizado seguro en HTML."""
    if not image_path or not isinstance(image_path, str):
        return None
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None
    return None

def efecto_carga(tipo="pregunta"):
    """Renderiza una animación de carga técnica."""
    msg = "ANALIZANDO CARACTERES..." if tipo == "pregunta" else "GENERANDO DIAGNÓSTICO TAXONÓMICO..."
    with st.empty():
        for percent_complete in range(0, 101, 20):
            time.sleep(0.1)  # Simulación de proceso
            st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div style="color: #58a6ff; font-family: monospace; font-size: 0.8rem; margin-bottom: 10px;">
                        {msg} {percent_complete}%
                    </div>
                    <div style="width: 100%; background: #161b22; border: 1px solid #30363d; height: 4px; border-radius: 2px;">
                        <div style="width: {percent_complete}%; background: #1f6feb; height: 100%; transition: width 0.2s;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.write("") # Limpia el spinner al terminar

def mostrar_sistema_experto():
    # --- SISTEMA DE DISEÑO TÉCNICO ---
    st.markdown("""
        <style>
            .stApp { background-color: #0d1117; }
            
            .status-bar {
                display: flex; justify-content: space-between; align-items: center;
                padding: 10px 20px; background: #161b22; border: 1px solid #30363d;
                border-radius: 6px; margin-bottom: 2rem;
            }
            .step-indicator {
                font-family: 'Inter', sans-serif; color: #8b949e;
                font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
            }

            .report-card {
                text-align: center; border: 1px solid #30363d;
                border-radius: 8px; background: #0d1117; overflow: hidden;
            }
            .report-header {
                background: #1f6feb; color: #ffffff; padding: 12px;
                font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
            }
            .scientific-name {
                font-size: 2.8rem; font-style: italic; font-weight: 600;
                color: #58a6ff; margin: 25px 0; font-family: 'Times New Roman', serif;
            }

            .specimen-frame {
                width: 100%; height: 450px; background-color: #010409;
                border: 1px solid #30363d; border-radius: 4px;
                display: flex; justify-content: center; align-items: center; overflow: hidden;
            }
            .specimen-frame img { max-width: 98%; max-height: 98%; object-fit: contain; }

            div.stButton > button {
                background: #21262d !important; color: #c9d1d9 !important;
                border: 1px solid #363b42 !important; padding: 1rem 1.5rem !important;
                border-radius: 6px !important; text-align: left !important;
                font-size: 0.95rem !important; width: 100% !important;
                transition: all 0.2s !important;
            }
            div.stButton > button:hover {
                background: #30363d !important; border-color: #8b949e !important;
                transform: translateX(5px);
            }
            
            .technical-note {
                padding: 15px; background: rgba(56, 139, 253, 0.1);
                border-left: 3px solid #1f6feb; color: #c9d1d9;
                font-size: 0.85rem; margin-top: 25px;
            }
        </style>
    """, unsafe_allow_html=True)

    kb = st.session_state.get('kb_dinamica', {})
    motor = MotorDeInferencia(kb)
    current = motor.obtener_actual()
    historial = st.session_state.get('history', [])
    paso_actual = len(historial) + 1

    # --- FLUJO 1: REPORTE DE IDENTIFICACIÓN ---
    if "resultado" in current:
        efecto_carga(tipo="resultado")
        img_b64 = get_base64_image(current.get("imagen", ""))
        
        st.markdown(f"""
            <div class="report-card">
                <div class="report-header">Informe de Identificación Taxonómica</div>
                <div style="padding: 40px;">
                    <span style="color: #8b949e; font-size: 0.75rem; font-weight: 600;">CLASIFICACIÓN FINAL</span>
                    <h1 class="scientific-name">{current['resultado']}</h1>
                    {f'<div class="specimen-frame"><img src="data:image/png;base64,{img_b64}"></div>' if img_b64 else ''}
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("INICIAR NUEVO PROTOCOLO", use_container_width=True):
                motor.reiniciar()
                st.rerun()
        return

    # --- FLUJO 2: PROTOCOLO DE EXAMEN ---
    
    st.markdown(f"""
        <div class="status-bar">
            <div class="step-indicator">Paso Actual: {paso_actual:02d}</div>
            <div class="step-indicator" style="color: #1f6feb;">Análisis Morfológico Activo</div>
        </div>
    """, unsafe_allow_html=True)

    col_data, col_view = st.columns([1, 1.2], gap="large")

    with col_data:
        st.markdown(f"""
            <div style="margin-bottom: 1.5rem;">
                <label style="color: #8b949e; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">Carácter en Evaluación:</label>
                <h3 style="color: #e6edf3; margin-top: 0.5rem; font-weight: 500; line-height: 1.4;">{current["pregunta"]}</h3>
            </div>
        """, unsafe_allow_html=True)

        for opcion in sorted(current["opciones"]):
            if st.button(opcion, key=f"opt_{opcion}_{paso_actual}"):
                efecto_carga(tipo="pregunta")
                motor.procesar(opcion)
                st.rerun()

        if paso_actual > 1:
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            if st.button("RETROCEDER AL CARÁCTER ANTERIOR"):
                motor.atras()
                st.rerun()

    with col_view:
        img_b64_ref = get_base64_image(current.get("imagen", ""))
        if img_b64_ref:
            st.markdown(f"""
                <div class="specimen-frame">
                    <img src="data:image/png;base64,{img_b64_ref}">
                </div>
                <p style="text-align: right; color: #8b949e; font-size: 0.65rem; margin-top: 8px; font-family: monospace;">REF_VISUAL_PASO_{paso_actual:02d}</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="specimen-frame" style="background: repeating-linear-gradient(45deg, #0d1117, #0d1117 10px, #161b22 10px, #161b22 20px);">
                    <span style="color: #30363d; font-size: 0.8rem; font-weight: 600;">SIN REGISTRO FOTOGRÁFICO</span>
                </div>
            """, unsafe_allow_html=True)

    if "nota" in current:
        st.markdown(f"""
            <div class="technical-note">
                <strong>Nota Técnica:</strong> {current["nota"]}
            </div>
        """, unsafe_allow_html=True)