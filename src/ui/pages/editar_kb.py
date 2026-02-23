import streamlit as st
import copy
import time

def interfaz_crear_pregunta():
    st.markdown("""
        <style>
            .stApp { background-color: #0d1117; }
            .editor-column {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 24px;
                height: 88vh;
                overflow-y: auto;
            }
            .tree-column {
                background: #090c10;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 20px;
                height: 88vh;
                overflow-y: auto;
            }
            .tech-label {
                color: #8b949e;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px;
            }
            /* Estilos del Árbol */
            .node-pregunta { color: #58a6ff; font-family: 'Roboto Mono', monospace; font-size: 0.85rem; margin-top: 10px; font-weight: bold; }
            .node-opcion { color: #8b949e; font-family: 'Roboto Mono', monospace; font-size: 0.8rem; border-left: 1px solid #30363d; padding-left: 10px; margin-left: 5px; }
            .node-resultado { color: #7ee787; font-family: 'Roboto Mono', monospace; font-size: 0.85rem; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    if "kb_dinamica" not in st.session_state:
        from src.data.base_de_conocimiento import BASE_DE_CONOCIMIENTO
        st.session_state.kb_dinamica = copy.deepcopy(BASE_DE_CONOCIMIENTO)

    if "nueva_pregunta" not in st.session_state:
        st.session_state.nueva_pregunta = {"texto": "", "nota": "", "imagen": "", "opciones": []}

    st.title("Sistema de Gestión de Claves Taxonómicas")
    
    col_input, col_view = st.columns([1.1, 1], gap="small")

    with col_input:
        st.markdown('<div class="editor-column">', unsafe_allow_html=True)
        
        # --- 01. LOCALIZACIÓN ---
        st.markdown('<p class="tech-label">01. Localización del Nodo</p>', unsafe_allow_html=True)
        
        def obtener_preguntas_y_opciones(kb):
            nodos = {}
            if "pregunta" in kb:
                pregunta_txt = kb["pregunta"]
                nodos[pregunta_txt] = list(kb.get("opciones", {}).keys())
                for subkb in kb.get("opciones", {}).values():
                    nodos.update(obtener_preguntas_y_opciones(subkb))
            return nodos

        dict_jerarquia = obtener_preguntas_y_opciones(st.session_state.kb_dinamica)
        padre_sel = st.selectbox("Pregunta Padre", ["-- Nodo Raíz --"] + list(dict_jerarquia.keys()))
        
        opcion_padre = None
        if padre_sel != "-- Nodo Raíz --":
            opcion_padre = st.selectbox("Colgar bajo la opción:", dict_jerarquia[padre_sel])

        # --- 02. CONFIGURACIÓN ---
        st.markdown('<p class="tech-label" style="margin-top:25px;">02. Configuración del Carácter</p>', unsafe_allow_html=True)
        texto_preg = st.text_input("Enunciado de la pregunta", st.session_state.nueva_pregunta["texto"])
        nota_preg = st.text_area("Nota técnica (protocolo)", st.session_state.nueva_pregunta["nota"], height=70)
        img_preg = st.text_input("Ruta de referencia visual", st.session_state.nueva_pregunta["imagen"])

        # --- 03. ESTADOS ---
        st.markdown('<p class="tech-label" style="margin-top:25px;">03. Estados Disponibles (Opciones)</p>', unsafe_allow_html=True)
        
        for i, opt in enumerate(st.session_state.nueva_pregunta["opciones"]):
            c_input, c_del = st.columns([0.9, 0.1])
            st.session_state.nueva_pregunta["opciones"][i] = c_input.text_input(f"Op {i}", opt, key=f"inp_{i}", label_visibility="collapsed")
            if c_del.button("×", key=f"del_{i}"):
                st.session_state.nueva_pregunta["opciones"].pop(i)
                st.rerun()

        if st.button("+ Añadir Estado del Carácter", use_container_width=True):
            st.session_state.nueva_pregunta["opciones"].append("")
            st.rerun()

        # --- 04. COMMIT ---
        st.write("")
        if st.button("SINCRONIZAR CON BASE DE DATOS", type="primary", use_container_width=True):
            if texto_preg and st.session_state.nueva_pregunta["opciones"]:
                nueva_estructura = {
                    "pregunta": texto_preg,
                    "nota": nota_preg,
                    "imagen": img_preg,
                    "opciones": {op: {} for op in st.session_state.nueva_pregunta["opciones"] if op}
                }

                def insertar_nodo(kb):
                    if padre_sel == "-- Nodo Raíz --":
                        st.session_state.kb_dinamica = nueva_estructura
                        return True
                    if kb.get("pregunta") == padre_sel:
                        kb["opciones"][opcion_padre] = nueva_estructura
                        return True
                    for sub in kb.get("opciones", {}).values():
                        if insertar_nodo(sub): return True
                    return False

                insertar_nodo(st.session_state.kb_dinamica)
                st.session_state.nueva_pregunta = {"texto": "", "nota": "", "imagen": "", "opciones": []}
                st.success("Estructura actualizada.")
                time.sleep(1)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_view:
        st.markdown('<p class="tech-label">Vista de Inspección Jerárquica</p>', unsafe_allow_html=True)
        st.markdown('<div class="tree-column">', unsafe_allow_html=True)
        
        def render_visual_tree(kb, indent=0):
            if "pregunta" in kb:
                st.markdown(f'<div class="node-pregunta" style="margin-left:{indent}px">P: {kb["pregunta"]}</div>', unsafe_allow_html=True)
                for op, sub in kb.get("opciones", {}).items():
                    st.markdown(f'<div class="node-opcion" style="margin-left:{indent+15}px">↳ O: {op}</div>', unsafe_allow_html=True)
                    render_visual_tree(sub, indent + 30)
            elif "resultado" in kb:
                st.markdown(f'<div class="node-resultado" style="margin-left:{indent}px">R: {kb["resultado"]}</div>', unsafe_allow_html=True)

        render_visual_tree(st.session_state.kb_dinamica)
        st.markdown('</div>', unsafe_allow_html=True)