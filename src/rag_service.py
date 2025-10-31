import pandas as pd
import os
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'Data', 'epi_r.csv','epi_r.csv')
##data = pd.read_csv(file_path)
##print(data.head())

def load_and_preprocess_data(file_path):
    """Carga, limpia y calcula la columna de carbohidratos del dataset de recetas."""
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {file_path}. Asegúrate de que el archivo esté en data/.")
        return None
    
    # 1. Eliminar filas con valores nulos en columnas críticas (macros)
    # y asegurarse de que los macros sean no-negativos
    cols_to_check = ['calories', 'protein', 'fat']
    data = data.dropna(subset=cols_to_check)
    data = data[(data[cols_to_check] >= 0).all(axis=1)]
    
    # 2. Calcular los gramos de carbohidratos
    # Carbs (g) = [Calories - (Protein * 4 + Fat * 9)] / 4
    data['carbs_g'] = (data['calories'] - (data['protein'] * 4 + data['fat'] * 9)) / 4
    
    # Opcional: Eliminar recetas con carbohidratos negativos (errores de datos)
    data = data[data['carbs_g'] >= 0]
    
    # Seleccionar solo las columnas que el Agente usará (macros y título)
    data = data[['title', 'calories', 'protein', 'fat', 'carbs_g']].copy()
    
    return data

def get_retriever_from_db(persist_directory: str = "chroma_db", collection_name: str = "recipe_collection"):
    """
    Carga la DB si existe. Si no, la crea desde el CSV preprocesado.
    Devuelve un objeto LangChain Retriever.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    persist_path = Path(persist_directory)
    persist_path.mkdir(parents=True, exist_ok=True)

    try:
        # Intenta cargar la base de datos persistente
        vectorstore = Chroma(
            collection_name=collection_name, 
            embedding_function=embeddings, 
            persist_directory=str(persist_path)
        )
        # Una pequeña verificación para ver si tiene documentos
        if vectorstore._collection.count() > 0:
            print(f"ChromaDB cargada exitosamente desde {persist_directory} (Documentos: {vectorstore._collection.count()})")
            return vectorstore.as_retriever()

    except Exception:
        pass 

    print("Creando nueva ChromaDB. Esto solo se hace una vez...")
    
    data_df = load_and_preprocess_data(file_path)
    if data_df is None or data_df.empty:
        raise Exception("No se pudieron cargar o preprocesar los datos para RAG.")

    loader = DataFrameLoader(data_df, page_content_column="title")
    documents = loader.load()
    bach_size = 5000
    vectorstore = Chroma.from_documents(
        documents=documents[0:bach_size], 
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=str(persist_path)
    )
    
    for i in range(bach_size,len(documents),bach_size):
        batch = documents[i:i + bach_size]
        print(f"Añadiendo lote {i // bach_size + 1}...")
        vectorstore.add_documents(batch)

    vectorstore.persist()
    print(f"✅ ChromaDB creada y persistida exitosamente en {persist_directory}")
    return vectorstore.as_retriever(search_kwargs={'k': 3})
