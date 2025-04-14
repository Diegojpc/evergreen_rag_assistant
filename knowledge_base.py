import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from config import VECTOR_DB_PATH, KNOWLEDGE_BASE_DIR, OPENAI_API_KEY

# --- Inicialización Singleton ---
# Para evitar recalcular embeddings o recargar la DB cada vez
_vector_db_instance = None
_embedding_function = None

def get_embedding_function():
    """Obtiene la función de embedding (singleton)."""
    global _embedding_function
    if _embedding_function is None:
        _embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return _embedding_function

def get_vector_db():
    """Obtiene la instancia de la Vector DB (singleton), inicializándola si es necesario."""
    global _vector_db_instance
    if _vector_db_instance is None:
        if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):
             print(f"Cargando Vector DB existente desde: {VECTOR_DB_PATH}")
             _vector_db_instance = Chroma(
                 persist_directory=VECTOR_DB_PATH,
                 embedding_function=get_embedding_function()
             )
        else:
            print("No se encontró Vector DB existente. Creando una nueva...")
            _vector_db_instance = setup_vector_db()
            if _vector_db_instance is None:
                 raise RuntimeError("Fallo al inicializar la base de datos vectorial.")
    return _vector_db_instance

def setup_vector_db():
    """Configura la base de datos vectorial por primera vez cargando documentos."""
    print(f"Cargando documentos desde: {KNOWLEDGE_BASE_DIR}")
    if not os.path.exists(KNOWLEDGE_BASE_DIR) or not os.listdir(KNOWLEDGE_BASE_DIR):
         print(f"Advertencia: El directorio de conocimiento '{KNOWLEDGE_BASE_DIR}' está vacío o no existe.")
         return None

    # Carga documentos desde el directorio especificado
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="*.txt", # Carga solo archivos .txt
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True # Puede acelerar la carga
    )
    documents = loader.load()

    if not documents:
        print("Advertencia: No se cargaron documentos.")
        return None

    print(f"Documentos cargados: {len(documents)}")

    # Divide los documentos en chunks más pequeños
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Tamaño del chunk (ajustar según necesidad)
        chunk_overlap=200   # Solapamiento entre chunks
    )
    texts = text_splitter.split_documents(documents)

    print(f"Documentos divididos en {len(texts)} chunks.")

    if not texts:
         print("Error: No se generaron chunks de texto.")
         return None

    # Crea la base de datos vectorial y persiste
    print("Creando embeddings y almacenando en ChromaDB...")
    try:
        db = Chroma.from_documents(
            texts,
            get_embedding_function(),
            persist_directory=VECTOR_DB_PATH
        )
        print(f"Vector DB creada y guardada en: {VECTOR_DB_PATH}")
        return db
    except Exception as e:
        print(f"Error creando la Vector DB: {e}")
        return None

def query_knowledge_base(query: str, k: int = 4) -> list:
    """Consulta la base de conocimiento vectorial."""
    db = get_vector_db()
    if db is None:
        print("Error: La base de datos vectorial no está inicializada.")
        return []
    try:
        # Realiza la búsqueda por similitud
        results = db.similarity_search(query, k=k)
        print(f"Recuperados {len(results)} documentos relevantes de la Vector DB.")
        # Devuelve el contenido de los documentos encontrados
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error al consultar la Vector DB: {e}")
        return []

# --- Función para inicializar al arrancar la app ---
def initialize_knowledge_base():
    """Función para llamar al inicio y asegurar que la DB esté lista."""
    print("Inicializando base de conocimiento...")
    get_vector_db() # Esto carga o crea la DB
    print("Base de conocimiento lista.")

if __name__ == "__main__":
    # Ejemplo de uso directo (para probar)
    initialize_knowledge_base()
    print("\n--- Probando consulta ---")
    test_query = "Recomendaciones de riego para tomates en floración"
    retrieved_docs = query_knowledge_base(test_query)
    if retrieved_docs:
        print(f"\nDocumentos recuperados para '{test_query}':")
        for i, doc in enumerate(retrieved_docs):
            print(f"--- Doc {i+1} ---")
            print(doc)
            print("-" * 20)
    else:
        print("No se recuperaron documentos.")