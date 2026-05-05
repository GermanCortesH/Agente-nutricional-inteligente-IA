# Agente Nutricional Inteligente (IA RAG)

## Visión General del Proyecto

Este proyecto implementa un agente de Inteligencia Artificial capaz de generar **planes y recomendaciones nutricionales personalizadas** en tiempo real. Utiliza la arquitectura **RAG (Retrieval-Augmented Generation)** con **LangChain** y **ChromaDB** para consultar una base de datos de recetas (*Knowledge Base*) antes de formular una respuesta con el modelo de lenguaje grande (LLM) **Llama 3** (a través de Ollama).

El objetivo es ofrecer planes dietéticos basados en parámetros específicos del usuario (calorías, proteínas, grasas, carbohidratos) y datos reales, garantizando respuestas informadas y precisas.

-----

## Características Clave

  * **Generación Aumentada (RAG):** El agente consulta una base de datos de recetas indexada en **ChromaDB** antes de generar la respuesta. Esto asegura que las recomendaciones sean factibles y específicas.
  * **Agente Conversacional:** Utiliza el framework **LangChain** para orquestar el flujo de trabajo entre la base de datos, el LLM y la herramienta de búsqueda.
  * **Base de Conocimiento:** Utiliza un *dataset* de recetas para construir la base de vectores, permitiendo al agente "recordar" las propiedades nutricionales de los alimentos.
  * **Tecnología LLM:** Implementado con el modelo **Llama 3** a través de **Ollama** para el despliegue local y eficiente.
  * **Interfaz Web:** Desarrollado con **Streamlit** para una interacción sencilla e intuitiva con el usuario.

-----

## Arquitectura del Sistema

El proyecto sigue un flujo RAG estándar de IA generativa:

1.  **Carga y Preprocesamiento:** Se carga un archivo de datos (ej: `epi_r.csv`).
2.  **Embeddings:** Se generan vectores (embeddings) de los títulos de las recetas usando **HuggingFace Embeddings**.
3.  **Vector Store (ChromaDB):** Los embeddings se almacenan en **ChromaDB** para una búsqueda rápida.
4.  **Consulta (LangChain/RetrievalQA):** Cuando el usuario pregunta, LangChain recupera las recetas más relevantes de ChromaDB.
5.  **Generación (Ollama/Llama 3):** El LLM recibe la pregunta original + las recetas recuperadas (contexto) y genera el plan nutricional personalizado.

-----

## Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en tu máquina.

### Prerrequisitos

1.  **Python 3.9+**

2.  **Ollama:** Asegúrate de tener **Ollama** instalado y corriendo, con el modelo `llama3:8b-instruct-q4_0` descargado.

    ```bash
    ollama pull llama3:8b-instruct-q4_0
    ```

### Pasos

1.  **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/GermanCortesH/Agente-nutricional-inteligente-IA.git
    cd Agente-nutricional-inteligente-IA
    ```

2.  **Crear y Activar el Entorno Virtual:**

    ```bash
    python -m venv entorno_ia
    # Windows:
    .\entorno_ia\Scripts\activate
    # Linux/macOS:
    source entorno_ia/bin/activate
    ```

3.  **Instalar Dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la Aplicación Streamlit:**

    ```bash
    streamlit run App.py
    ```

La aplicación se abrirá automáticamente en tu navegador. Al iniciar por primera vez, se creará la base de datos `chroma_db/`.

-----

## Contribuciones

Si tienes sugerencias para mejorar el *prompt*, añadir más herramientas o incluir bases de datos más grandes, ¡tus contribuciones son bienvenidas\!

1.  Haz un `Fork` del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3.  Confirma tus cambios (`git commit -m 'feat: Añadir mejora X'`).
4.  Haz `Push` a tu rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un `Pull Request`.

-----

> Creado por **[German Cortes H.]**
