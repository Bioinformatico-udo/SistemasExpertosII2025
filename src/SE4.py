import streamlit as st

BASE_DE_CONOCIMIENTO = {
    "pregunta": "¿El telson es largo (al menos la mitad de la longitud del caparazón)?",
    "si": {
        "nota": "Esta característica define a la familia Hippidae.",
        "pregunta": "¿El flagelo antenal es más corto que las anténulas?",
        "si": {
            "nota": "Género Hippa. H. testudinaria es la única especie de este género en el Caribe.",
            "resultado": "Hippa testudinaria"
        },
        "no": {
            "nota": "Género Emerita. La identificación en este punto es crítica por variabilidad morfológica.",
            "pregunta": "¿Los dáctilos del primer par de pereiópodos son redondeados?",
            "si": {
                "nota": "Históricamente identificada como E. brasiliensis, aunque estudios recientes sugieren posibles errores de identificación en Venezuela.",
                "resultado": "Emerita brasiliensis"
            },
            "no": {
                "nota": "La forma aguda del dáctilo es diagnóstica, pero variable en ejemplares jóvenes.",
                "resultado": "Emerita portoricensis"
            }
        }
    },
    "no": {
        "nota": "Un telson corto (mucho menos de la mitad del caparazón) define a Albuneidae.",
        "pregunta": "¿El margen anterior del caparazón es claramente aserrado?",
        "si": {
            "nota": "Género Albunea. Poseen ojos subtriangulares.",
            "pregunta": "¿El dáctilo del cuarto par presenta una depresión brusca en su margen posterior?",
            "si": {
                "nota": "Representa una nueva adición a la carcinofauna de Venezuela.",
                "resultado": "Albunea catherinae"
            },
            "no": {
                "nota": "Depresión gradual. Podría confundirse con A. gibbesii (talón del 3er pereiópodo redondeado), aún no hallada en el país.",
                "resultado": "Albunea paretii"
            }
        },
        "no": {
            "nota": "Género Lepidopa. El margen anterior es liso.",
            "pregunta": "¿Los ojos y pedúnculos oculares son subovalados?",
            "si": {
                "nota": "Para confirmar, el talón del dáctilo del 2do pereiópodo debe ser agudo (en L. luciae es redondeado).",
                "resultado": "Lepidopa venusta"
            },
            "no": {
                "nota": "Los ojos en esta especie se describen como subcuadrados o subrectangulares.",
                "resultado": "Lepidopa richmondi"
            }
        }
    }
}



class MotorDeInferencia:
    def __init__(self, kb):
        self.kb = kb
        if "history" not in st.session_state:
            st.session_state.history = [self.kb]

    def obtener_actual(self):
        return st.session_state.history[-1]

    def procesar(self, answer):
        current_node = self.obtener_actual()
        if answer in current_node:
            st.session_state.history.append(current_node[answer])

    def atras(self):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()

    def reiniciar(self):
        st.session_state.history = [self.kb]


def main():
    st.title("Sistema Experto")
    
    motor = MotorDeInferencia(BASE_DE_CONOCIMIENTO)
    current = motor.obtener_actual()

    if "nota" in current:
        st.info(current["nota"])

    if "resultado" in current:
        st.success(f"### Especie: {current['resultado']}")
        if st.button("Reiniciar"):
            motor.reiniciar()
            st.rerun()
    else:
        st.write(f"#### {current['pregunta']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("SÍ", use_container_width=True):
                motor.procesar("si")
                st.rerun()
        with col2:
            if st.button("NO", use_container_width=True):
                motor.procesar("no")
                st.rerun()

        if len(st.session_state.history) > 1:
            st.button("← Volver", on_click=motor.atras)

if __name__ == "__main__":
    main()