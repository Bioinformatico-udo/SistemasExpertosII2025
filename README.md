#Sistema Experto de Identificación de Crustáceos
-Este proyecto es una aplicación web interactiva desarrollada con Streamlit. Utiliza un motor de inferencia basado en una base de conocimiento dicotómica para identificar especies de crustáceos (específicamente de las familias Hippidae y Albuneidae) presentes en las costas de Venezuela y el Caribe.

#Características
-Motor de Inferencia Progresivo: Avanza a través de preguntas binarias (Sí/No) basadas en morfología.

-Notas Taxonómicas: Proporciona información adicional y advertencias críticas sobre cada paso de la identificación.

-Gestión de Estado: Permite retroceder a la pregunta anterior o reiniciar el proceso sin recargar la página.

-Interfaz Intuitiva: Diseño limpio utilizando columnas y componentes nativos de Streamlit.

#Estructura del Código
-BASE_DE_CONOCIMIENTO: Un diccionario anidado que representa el árbol de decisión taxonómico.

-MotorDeInferencia: Clase encargada de gestionar la lógica de navegación y el historial de pasos mediante st.session_state.

-main(): Función principal que renderiza la interfaz de usuario y captura las entradas del usuario.

#Instalación y Uso
-Requisitos previos:
-Asegúrate de tener instalado Python y Streamlit:

Bash
pip install streamlit
Ejecución:
Guarda el código en un archivo llamado app.py y ejecútalo con el siguiente comando:

Bash
streamlit run app.py