import streamlit as st
def mostrar_inicio():
    st.title("Sistema Experto HippoCaribe 📖")

    st.markdown("""
    Bienvenido al sistema experto para la identificación de crustáceos
    del Caribe venezolano.

    Este sistema utiliza una base de conocimiento construida a partir de
    claves dicotómicas, permitiendo determinar la especie mediante una
    secuencia de preguntas sobre características morfológicas.
    """)

    st.markdown("---")

    st.subheader("¿Qué puedes hacer aquí?")

    st.markdown("""
    - Identificar especies de crustáceos mediante preguntas guiadas  
    - Consultar información básica durante el proceso  
    - Conocer al equipo desarrollador en la sección Portafolio  
    """)

    st.markdown("---")

    st.write("""
Este proyecto surge como una respuesta a la necesidad de modernizar las herramientas de determinación taxonómica en Venezuela. Aprovechando el reciente inventario actualizado de la superfamilia Hippoidea, que eleva a siete el número de especies registradas en el país (representando el 58,33% de la diversidad del Caribe), este sistema experto digitaliza el conocimiento científico de vanguardia para hacerlo accesible e interactivo.
¿Por qué Hippoidea?
Los llamados "cangrejos topo" son piezas fundamentales de la infauna de nuestras playas arenosas. Sin embargo, su identificación representa un desafío técnico, ya que requiere observar detalles morfológicos precisos —como la forma de los pedúnculos oculares, la longitud del telson o la curvatura de los dáctilos— que a menudo confunden a los no especialistas.


Nuestra Solución: Python + Streamlit
             
Utilizando un enfoque de lógica dicotómica, nuestro sistema guía al usuario a través de un árbol de decisión dinámico basado en las claves ilustradas de las fuentes más recientes:
             
• Interfaz Interactiva: Desarrollada en Streamlit, permite una navegación fluida donde el usuario responde a preguntas sucesivas sobre características físicas observables.
             
• Rigor Científico: El motor del sistema integra los diagnósticos de las familias Albuneidae e Hippidae, diferenciándolas por la proporción del telson respecto al caparazón.
             
• Actualización en Tiempo Real: El sistema incluye registros históricos y nuevos hitos de la biodiversidad venezolana, como la reciente adición de Albunea catherinae hallada en la isla La Tortuga.
             
• Manejo de Ambigüedades: Incorpora notas técnicas sobre especies con alta variabilidad morfológica, como las del género Emerita, donde la forma de los dáctilos puede variar según la edad del ejemplar.
             
Este sistema no solo reduce el margen de error en la identificación de especies crípticas, sino que se posiciona como una herramienta educativa y de investigación esencial para el estudio de la biodiversidad marina en las costas venezolanas
    """)

    st.info("Utiliza  HippoCaribe en el menú lateral para comenzar.")
