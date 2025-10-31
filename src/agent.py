## codigo para generar un agente que ayude a planificar rutinas de alimentacion con IA
from langchain.tools import tool
import src.agent_tools as mt 
import src.rag_service as rag
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

@tool
def calcular_tmb(peso: float, altura: float, edad: int, genero: str) -> float:
    """Calcula la Tasa Metabólica Basal (TMB) del usuario utilizando la fórmula de Mifflin-St Jeor.

    Args:
        peso: El peso del usuario en kilogramos (kg).
        altura: La altura del usuario en centímetros (cm).
        edad: La edad del usuario en años.
        genero: El género biológico ("hombre" o "mujer").

    Returns:
        tmb: La Tasa Metabólica Basal calculada en calorías (kcal).
    """
    return mt.calcular_tmb(peso, altura, edad, genero)

@tool
def calcular_tdee(tmb: float, nivel_actividad: str) -> float:
    """Calcula el Gasto Energético Diario Total (TDEE) ajustando la TMB por el factor de actividad.

    Args:
        tmb: La Tasa Metabólica Basal calculada previamente (kcal).
        nivel_actividad: El nivel de actividad física ("sedentario", "ligero", "moderado", "intenso", "muy intenso").

    Returns:
        tdee: El Gasto Energético Diario Total en calorías (kcal).
    """
    return mt.calcular_tdee(tmb, nivel_actividad)

@tool
def calcular_macros(tdee: float, objetivo: str) -> dict:
    """Calcula el objetivo calórico final y la distribución de macronutrientes (Proteínas, Carbohidratos, Grasas) en gramos.

    Args:
        tdee: El Gasto Energético Diario Total (kcal).
        objetivo: El objetivo del usuario ("perder peso", "ganar peso", "mantener peso").

    Returns:
        Un diccionario con los objetivos nutricionales: {"calorias": float, "proteinas_g": float, "grasas_g": float, "carbohidratos_g": float}.
    """
    return mt.calcular_macros(tdee, objetivo)

recetas_busqueda = rag.get_retriever_from_db()
@tool
def busqueda_recetas(query: str) -> str:
    """Busca recetas en la base de datos de recetas (RAG) que cumplen con los requisitos nutricionales.
    
    El Agente debe usar los GRAMOS de Proteínas, Carbohidratos y Grasas calculados previamente 
    para formular una consulta de búsqueda semántica. La consulta debe ser un resumen
    del tipo de receta (ej: "Recetas con más de 100g de proteína y menos de 50g de carbohidratos, tipo cena").

    Args:
        query: Una cadena de texto descriptiva de los requisitos de la receta y tipo de comida.
        
    Returns:
        Una lista de las recetas más relevantes y sus metadatos de macros (título, calorías, protein_g, etc.) 
        en formato JSON para que el agente pueda generar el plan.
    """
    recetas_busqueda.retrieve(query)
    results = [f"Título: {doc.page_content}, Macros: {doc.metadata}" for doc in docs]
    return "\n".join(results)

calculation_tools = [calcular_tmb, calcular_tdee, calcular_macros]

SYSTEM_PROMPT = """
Tu rol es el de un Agente Nutricional Inteligente (ANI), un dietista y planificador de comidas experto.
Tu objetivo es crear un plan nutricional semanal personalizado y detallado para el usuario.
Usa la siguiente información para responder a la pregunta del usuario.
Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.

Contexto: {context}
Pregunta: {question}

SIGUE ESTOS PASOS RIGUROSAMENTE:
1. ANÁLISIS METABÓLICO: Debes usar las herramientas 'calcular_tmb', 'calcular_tdee' y 'calcular_macros' en ese orden. Extrae los datos (peso, altura, edad, género, nivel_actividad, objetivo) de la solicitud del usuario para calcular el OBJETIVO CALÓRICO FINAL y los GRAMOS de Proteínas, Carbohidratos y Grasas.
2. BÚSQUEDA DE RECETAS: Utiliza la herramienta 'search_recipes' una sola vez. En tu consulta ('query'), debes incluir el tipo de comidas que necesitas (desayuno, almuerzo, cena) y los objetivos de MACROS CALCULADOS (Proteínas, Carbohidratos, Grasas) para obtener recetas que encajen.
3. GENERACIÓN DEL PLAN: Una vez que tengas los macros objetivos y el listado de recetas relevantes de la herramienta de búsqueda, presenta el plan final.

FORMATO DE SALIDA REQUERIDO:
Presenta tu respuesta final directamente al usuario en español, con un tono motivador y experto.
Muestra primero un resumen del Análisis Metabólico (TDEE, Calorías Objetivo y Gramos de Macros).
Luego, genera un PLAN SEMANAL (7 días) de comidas. Para cada día, propone 3 comidas (Desayuno, Almuerzo, Cena) basadas en las recetas encontradas.

IMPORTANTE: Justifica por qué las recetas elegidas son adecuadas para su objetivo nutricional.
"""

tools = calculation_tools + [busqueda_recetas]

def create_nutrition_agent():
    """Configura y devuelve el ejecutor final del Agente Nutricional Inteligente."""
    
    # 2. Inicializar el LLM de Ollama
    # Usamos llama3 (debes asegurarte de que esté instalado via 'ollama pull llama3')
    llm = Ollama(model="llama3:8b-instruct-q4_0") 

    # 3. Construir el Prompt final del Agente
    # Utilizamos MessagesPlaceholder para que LangChain maneje el historial de la conversación 
    # y la inyección de los pasos de Tool Calling.
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", SYSTEM_PROMPT),
    #         MessagesPlaceholder(variable_name="chat_history"),
    #         ("human", "{input}"),
    #         MessagesPlaceholder(variable_name="agent_scratchpad"),
    #     ]
    # )
    prompt = PromptTemplate(template=SYSTEM_PROMPT,
                        input_variables=['context', 'question'])

    agent_executor = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=rag.get_retriever_from_db(),
                                    return_source_documents=True,
                                    verbose=True,
                                    chain_type_kwargs={"prompt": prompt})
    return agent_executor