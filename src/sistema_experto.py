import streamlit as st
from motor_de_inferencia import MotorDeInferencia

def mostrar_sistema_experto():
    st.title("Sistema Experto HippoCaribe")

    motor = MotorDeInferencia(st.session_state.kb_dinamica)
    current = motor.obtener_actual()

    if "imagen" in current:
        st.image(current["imagen"], use_container_width=True)

    if "nota" in current:
        st.info(current["nota"])

    if "resultado" in current:
        st.success(f"### Especie identificada: {current['resultado']}")
        if st.button("Reiniciar"):
            motor.reiniciar()
            st.rerun()
        return

    st.subheader(current["pregunta"])

    for opcion in current["opciones"]:
        if st.button(opcion, use_container_width=True):
            motor.procesar(opcion)
            st.rerun()

    if len(st.session_state.history) > 1:
        st.button("← Volver", on_click=motor.atras)
