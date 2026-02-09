import streamlit as st
class MotorDeInferencia:
    def __init__(self, kb):
        self.kb = kb
        if "history" not in st.session_state:
            st.session_state.history = [self.kb]

    def obtener_actual(self):
        return st.session_state.history[-1]

    def procesar(self, opcion):
        current = self.obtener_actual()
        if "opciones" in current and opcion in current["opciones"]:
            st.session_state.history.append(current["opciones"][opcion])

    def atras(self):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()

    def reiniciar(self):
        st.session_state.history = [self.kb]
