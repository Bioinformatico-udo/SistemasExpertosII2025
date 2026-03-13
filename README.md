# Mi Sistema Experto de Porcelánidos 🦀

¡Bienvenido a mi proyecto! Este es un **Sistema Experto Híbrido** diseñado para identificar especies de cangrejos porcelánidos en Venezuela. Lo he construido combinando reglas taxonómicas tradicionales con inteligencia artificial (Machine Learning).

## 🚀 ¿Qué hace este sistema?

He creado una herramienta que ayuda a identificar qué especie de cangrejo tienes enfrente basándose en sus características físicas (morfología).

Lo especial de mi sistema es que utiliza **dos estrategias** para razonar:

1.  **Reglas de Expertos (Kommonkads)**: Utiliza el conocimiento de taxónomos para seguir reglas estrictas ("Si tiene esto y esto, entonces es tal especie").
2.  **Inteligencia Artificial (Machine Learning)**: Si las reglas no son suficientes, uso un modelo de Árbol de Decisión entrenado con datos reales para sugerir la especie más probable.

## 🧠 Modos de Inferencia

He implementado dos formas de usar el cerebro del sistema:

### 1. Forward Chaining (Hacia Adelante)
*   **¿Cuándo lo uso?** Cuando tengo un cangrejo y **no tengo idea** de qué especie es.
*   **¿Qué hace?** Evalúa todas las reglas posibles y me da una lista de candidatos ordenados por probabilidad.
*   **En la Interfaz:** Selecciono "Forward", meto los datos, y el sistema me dice: "Puede ser A (100%) o B (20%)".

### 2. Backward Chaining (Hacia Atrás)
*   **¿Cuándo lo uso?** Cuando tengo una sospecha ("Creo que esto es un *Porcellana sp. A*") y quiero confirmarlo.
*   **¿Qué hace?** Busca solo las reglas de esa especie específica y verifica si el espécimen las cumple.
*   **En la Interfaz:** Selecciono "Backward", elijo la especie, y el sistema me responde: "SÍ, cumple" o "NO, falla en esto".

## 📂 ¿Cómo está organizado mi código?

He tratado de mantener todo muy ordenado:

*   **`src/`**: Aquí está todo el código fuente.
    *   **`ui/`**: La interfaz gráfica donde interactúo con el sistema.
    *   **`motor_reglas/`**: El cerebro lógico con las reglas taxonómicas.
    *   **`ml/`**: El cerebro estadístico (Machine Learning).
    *   **`datos/`** y **`caracteristicas/`**: Scripts para limpiar y preparar los datos.
*   **`data/`**: Aquí guardo mis datos.
    *   **`raw/`**: Datos crudos originales (¡estos no se tocan!).
    *   **`processed/`**: Datos limpios y listos para usar con el modelo ML.
*   **`models/`**: Aquí se guarda el modelo entrenado (`.joblib`).

## 🛠️ Instalación y Uso (Windows)

Para ponerlo a funcionar en mi máquina, sigo estos pasos:

1.  **Crear un entorno virtual** (para no mezclar librerías):
    ```powershell
    py -3.14 -m venv .venv
    ```

2.  **Activarlo**:
    ```powershell
    .venv\Scripts\Activate.ps1
    ```

3.  **Instalar lo necesario**:
    ```powershell
    pip install -r requirements.txt
    ```

4.  **¡Listo! Para abrir la Interfaz**:
    ```powershell
    py -m src.ui.app
    ```

### Otros comandos útiles que uso:

*   **Entrenar el modelo de nuevo**:
    ```powershell
    py -m src.ml.entrenar data/processed/porcellanids_processed.csv
    ```
*   **Correr los tests** (para ver que no rompí nada):
    ```powershell
    py -m pytest
    ```
    ```powershell
    py -m src.ml.visualizar_arbol
    ```
    *Esto mostrará en la consola el mapa lógico detallado de cómo el sistema toma decisiones.*

## 📖 Mi pequeño Glosario

Para no perderme con los términos biológicos:

*   **Rostro**: La "nariz" o punta del caparazón. Mido desde la base hasta la punta.
*   **Carapacho**: El caparazón dorsal. Me fijo si es liso (*smooth*) o rugoso.
*   **Quelas**: Las pinzas grandes. Son clave para identificar.
*   **Pleon**: El abdomen. En estos cangrejos suele estar plegado abajo.
*   **Setas**: Pelitos sensoriales. A veces importan.

## 📚 Fuentes de Información

Los datos morfológicos de las 11 especies para realizar este sistema experto fueron recopilados de las siguientes fuentes científicas autorizadas:

*   **WoRMS (World Register of Marine Species)**: [http://www.marinespecies.org](http://www.marinespecies.org) - Para la validación taxonómica y nombres aceptados.
*   **GBIF (Global Biodiversity Information Facility)**: [https://www.gbif.org](https://www.gbif.org) - Para datos de distribución y registros de especímenes.
*   **Scielo Venezuela / Saber ULA**: Investigaciones locales sobre crustáceos decápodos.
    *   *Rodríguez, G. (1980)*. "Los crustáceos decápodos de Venezuela". Instituto Venezolano de Investigaciones Científicas.
    *   *Lira, C. (2004)*. "Estudios sobre porcelánidos del Caribe venezolano".

Cada especie en el archivo `especies_venezuela.csv` incluye notas específicas extraídas de estas referencias para justificar las reglas del sistema experto.

---
*Este sistema fue desarrollado siguiendo la metodología **Kommonkads** para estandarizar cómo medimos y clasificamos estas especies.*
