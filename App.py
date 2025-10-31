import streamlit as st
from src.agent import create_nutrition_agent

@st.cache_resource
def get_agent_executor():
    """Inicializa y cachea el AgentExecutor de LangChain."""
    return create_nutrition_agent()

agent_executor = get_agent_executor()

st.set_page_config(page_title="Agente Nutricional Inteligente", layout="wide")
st.title("Agente Nutricional Inteligente")
st.markdown("Introduce tus datos y tu objetivo para recibir un plan nutricional semanal personalizado.")

with st.sidebar:
    st.header("Datos Biométricos")
    
    # Datos Numéricos
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.5)
    altura = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0)
    edad = st.number_input("Edad (años)", min_value=18, max_value=100, value=30)
    
    genero = st.selectbox(
        "Género",
        ["Hombre", "Mujer"]
    ).lower() 
    
    nivel_actividad = st.selectbox(
        "Nivel de Actividad",
        ["sedentario", "ligero", "moderado", "intenso", "muy intenso"]
    ).lower()

    st.header("Objetivo Nutricional")
    objetivo = st.selectbox(
        "Objetivo",
        ["perder peso", "ganar peso", "mantener peso"]
    ).lower()

    st.markdown("---")
    
    query = f"""
    Quiero lograr el objetivo de **{objetivo}**. 
    Mis datos son: Peso={peso} kg, Altura={altura} cm, Edad={edad} años, Género={genero}. 
    Mi nivel de actividad es **{nivel_actividad}**. 
    Por favor, usa tus herramientas para calcular mis macros y luego genera mi plan semanal.
    """
    
    if st.button("Generar Plan Nutricional", type="primary"):
        if peso > 0 and altura > 0:
            st.session_state['run_query'] = True
        else:
            st.error("Por favor, introduce Peso y Altura válidos.")


if 'run_query' in st.session_state and st.session_state['run_query']:
    st.subheader("Planificación del Agente 🧠")
    
    with st.spinner("El Agente está calculando tu TDEE, macros y buscando recetas..."):
        try:
            result = agent_executor.invoke({"query": query, "chat_history": []})

        
            st.success("¡Plan Generado Exitosamente!")
            st.markdown("---")
            st.write("Claves devueltas por el agente:")
            st.json(result.keys()) 
            st.json(result) 
            #st.markdown(result["result"])
            
        except Exception as e:
            st.error(f"Ocurrió un error en la ejecución del agente. Asegúrate de que Ollama (llama3) esté corriendo. Error: {e}")
            st.markdown("**Consejo:** Revisa la consola de LangChain (si `verbose=True`) para ver el error de *Tool Calling*.")
        
    st.session_state['run_query'] = False