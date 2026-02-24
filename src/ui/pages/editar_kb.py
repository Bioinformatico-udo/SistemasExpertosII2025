import streamlit as st
import json
import os
import time

PATH_JSON = "src/data/base_de_conocimiento.json"

def cargar_kb():
    if os.path.exists(PATH_JSON):
        with open(PATH_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_kb(datos):
    os.makedirs(os.path.dirname(PATH_JSON), exist_ok=True)
    with open(PATH_JSON, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def obtener_todos_los_nodos(kb, nodos=None):
    if nodos is None: nodos = {}
    if "pregunta" in kb:
        nodos[kb["pregunta"]] = kb
        for opcion in kb.get("opciones", {}).values():
            obtener_todos_los_nodos(opcion, nodos)
    elif "resultado" in kb:
        nodos[f"🦀 {kb['resultado']}"] = kb
    return nodos

@st.dialog("Estado del Sistema")
def ventana_exito_guardado():
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
            <i class="bi bi-check-circle-fill" style="font-size: 4rem; color: #238636;"></i>
            <h2 style="color: white; margin-top: 15px;">¡Guardado con éxito!</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.rerun()

@st.dialog("Confirmar Eliminación")
def ventana_confirmar_borrado(item_nombre):
    st.markdown(f"""
        <div style="text-align: center;">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
            <i class="bi bi-trash" style="font-size: 3.5rem; color: #ff4b4b;"></i>
            <p style="font-size: 1.2rem; margin-top: 15px;">¿Deseas eliminar permanentemente:<br><b>"{item_nombre}"</b>?</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    if c1.button("SÍ, ELIMINAR", use_container_width=True):
        def eliminar_recursivo(kb, target):
            if "opciones" in kb:
                for op, sub in list(kb["opciones"].items()):
                    if sub.get("pregunta") == target or f"🦀 {sub.get('resultado')}" == target:
                        kb["opciones"][op] = {}
                        return True
                    if eliminar_recursivo(sub, target): return True
            return False
        
        eliminar_recursivo(st.session_state.kb_dinamica, item_nombre)
        guardar_kb(st.session_state.kb_dinamica)
        st.rerun()
        
    if c2.button("CANCELAR", use_container_width=True):
        st.rerun()

    st.components.v1.html("""
        <script>
            const btns = window.parent.document.querySelectorAll('button');
            btns.forEach(btn => {
                if (btn.innerText.includes("SÍ, ELIMINAR")) {
                    btn.style.backgroundColor = "#da3633";
                    btn.style.color = "white";
                    btn.style.border = "1px solid #f85149";
                }
            });
        </script>
    """, height=0)

def interfaz_crear_pregunta():
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
        <style>
            .scroll-container { background: #090c10; border: 1px solid #30363d; border-radius: 8px; padding: 20px; height: 600px; overflow-y: auto; }
            .tree-branch { border-left: 1px solid #30363d; margin-left: 10px; padding-left: 15px; margin-top: 5px; }
            .node-pregunta { color: #58a6ff; font-weight: bold; font-size: 0.85rem; margin-top: 10px; }
            .node-opcion { color: #8b949e; font-size: 0.8rem; margin-top: 2px; }
            .node-resultado { color: #7ee787; font-weight: bold; font-size: 0.85rem; margin-top: 5px; }
            
            div.stButton > button:first-child[kind="primary"] {
                background-color: #238636 !important;
                border-color: #2ea043 !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if "kb_dinamica" not in st.session_state:
        st.session_state.kb_dinamica = cargar_kb()

    st.title("🦀 Gestión HippoCaribe")
    
    col_input, col_view = st.columns([1, 1], gap="medium")

    with col_input:
        with st.container(border=True):
            todos_los_nodos = obtener_todos_los_nodos(st.session_state.kb_dinamica)
            modo = st.radio("Acción:", ["Editar existente", "Insertar Nodo Taxonómico"], horizontal=True)
            
            if modo == "Editar existente":
                seleccion = st.selectbox("Nodo:", list(todos_los_nodos.keys()))
                nodo_actual = todos_los_nodos.get(seleccion, {})
            else:
                padre_sel = st.selectbox("Nodo de Referencia:", [k for k in todos_los_nodos.keys() if "🦀" not in k])
                opcion_donde_colgar = st.selectbox("Bajo:", list(todos_los_nodos.get(padre_sel, {}).get("opciones", {}).keys()))
                nodo_actual = {} 

            tipo_nodo = st.radio("Tipo:", ["Pregunta", "Especie"], index=1 if "resultado" in nodo_actual else 0, horizontal=True)

            if tipo_nodo == "Pregunta":
                texto = st.text_input("Enunciado", nodo_actual.get("pregunta", ""))
                nota = st.text_area("Nota técnica", nodo_actual.get("nota", ""), height=70)
                img = st.text_input("Imagen URL", nodo_actual.get("imagen", ""))
                ops = st.text_input("Opciones (comas)", ", ".join(nodo_actual.get("opciones", {}).keys()) if "opciones" in nodo_actual else "")
                list_ops = [o.strip() for o in ops.split(",") if o.strip()]
                datos = {"pregunta": texto, "nota": nota, "imagen": img, "opciones": {o: nodo_actual.get("opciones", {}).get(o, {}) for o in list_ops}}
            else:
                texto = st.text_input("Nombre Especie", nodo_actual.get("resultado", ""))
                nota = st.text_area("Descripción", nodo_actual.get("nota", ""), height=70)
                img = st.text_input("Imagen URL", nodo_actual.get("imagen", ""))
                datos = {"resultado": texto, "nota": nota, "imagen": img}

            st.write("")
            c1, c2 = st.columns(2)
            
            if c1.button("GUARDAR", type="primary", use_container_width=True):
                if texto:
                    if modo == "Editar existente":
                        nodo_actual.clear()
                        nodo_actual.update(datos)
                    else:
                        todos_los_nodos[padre_sel]["opciones"][opcion_donde_colgar] = datos
                    guardar_kb(st.session_state.kb_dinamica)
                    ventana_exito_guardado()

            if modo == "Editar existente":
                if c2.button("ELIMINAR", use_container_width=True):
                    ventana_confirmar_borrado(seleccion)
                
                st.components.v1.html(f"""
                    <script>
                        function applyStyles() {{
                            const buttons = window.parent.document.querySelectorAll('button');
                            buttons.forEach(btn => {{
                                if (btn.innerText.includes("GUARDAR")) {{
                                    btn.innerHTML = '<i class="bi bi-floppy" style="margin-right: 8px;"></i> GUARDAR';
                                }}
                                if (btn.innerText.includes("ELIMINAR")) {{
                                    btn.innerHTML = '<i class="bi bi-trash" style="margin-right: 8px;"></i> ELIMINAR';
                                    btn.style.backgroundColor = "#da3633";
                                    btn.style.color = "white";
                                    btn.style.border = "1px solid #f85149";
                                }}
                                if (btn.innerText.includes("SÍ, ELIMINAR")) {{
                                    btn.style.backgroundColor = "#da3633";
                                    btn.style.color = "white";
                                }}
                            }});
                        }}
                        applyStyles();
                        setTimeout(applyStyles, 300); // Doble chequeo para asegurar el color
                    </script>
                """, height=0)

    with col_view:
        with st.container(border=True):
            def arbol(kb):
                h = ""
                if "pregunta" in kb:
                    h += f'<div class="node-pregunta">❓ {kb["pregunta"]}</div><div class="tree-branch">'
                    for o, s in kb.get("opciones", {}).items():
                        h += f'<div class="node-opcion">↳ <b>{o}</b></div>{arbol(s)}'
                    h += '</div>'
                elif "resultado" in kb: h += f'<div class="node-resultado">🦀 {kb["resultado"]}</div>'
                return h
            st.markdown(f'<div class="scroll-container">{arbol(st.session_state.kb_dinamica)}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    interfaz_crear_pregunta()