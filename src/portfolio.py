import streamlit as st

def mostrar_portafolio():
    st.title("Contacto 👤")

    st.subheader("Integrantes")

    st.markdown("""
    **Integrante 1:** Anghelo Aguilera  
    Portafolio: https://portfolioangheloaguilera.vercel.app/ 

    **Integrante 2:** Josue Cabeza   
    Portafolio: https://tuportafolio2.com  

    **Integrante 3:** Yuhan Picos     
    Portafolio: https://portfolio-yuhanpicos.vercel.app/ 
    """)

    st.markdown("---")

    st.subheader("Proyecto 📝")


    st.markdown("**Tecnologías utilizadas:** Python, Streamlit")

    st.markdown("---")

    st.subheader("Observaciones")

    st.write("""
    Cada integrante participó en el diseño lógico del sistema,
    construcción de la base de conocimiento y desarrollo de la interfaz.
    """)
