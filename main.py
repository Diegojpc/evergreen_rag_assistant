# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json # Para serializar la respuesta si es necesario

from config import OPENAI_API_KEY # Para verificar que esté cargada
from knowledge_base import initialize_knowledge_base
from rag_core import get_recommendations, RagResponse # Importa la función principal y el modelo de respuesta

# --- Modelo de Datos para la Solicitud API ---
class RecommendationRequest(BaseModel):
    project_id: str
    user_query: str = "¿Qué acciones debo realizar en mi cultivo durante los próximos 5-7 días?" # Query por defecto

# --- Inicialización de la Aplicación FastAPI ---
app = FastAPI(
    title="Evergreen RAG Assistant API",
    description="API para obtener recomendaciones de gestión de cultivos usando RAG.",
    version="0.1.0"
)

# --- Evento de Inicio ---
# Se ejecuta una vez cuando FastAPI arranca
@app.on_event("startup")
async def startup_event():
    print("Iniciando API...")
    if not OPENAI_API_KEY:
         print("ERROR CRÍTICO: La clave API de OpenAI no está configurada. La API no funcionará correctamente.")
         # Podrías lanzar una excepción aquí para detener el inicio si es necesario
         # raise RuntimeError("OpenAI API Key not found!")
    else:
         print("Clave API de OpenAI encontrada.")
    # Inicializa la base de conocimiento (carga o crea la Vector DB)
    initialize_knowledge_base()
    print("API lista para recibir solicitudes.")


# --- Endpoint de la API ---
# Definimos que la respuesta será del tipo RagResponse o un dict (para errores)
@app.post("/generate_recommendation",
          response_model=RagResponse, # FastAPI usará esto para validar y documentar la respuesta exitosa
          summary="Genera Recomendaciones para un Cultivo",
          description="Recibe un ID de proyecto y una consulta (opcional), y devuelve recomendaciones, alertas y justificaciones.")
async def generate_recommendation_endpoint(request: RecommendationRequest):
    """
    Endpoint principal para obtener recomendaciones agronómicas.

    - **project_id**: Identificador único del proyecto/cultivo en Evergreen.
    - **user_query**: Pregunta específica del usuario o descripción de la necesidad (opcional, usa valor por defecto si no se provee).
    """
    print(f"Recibida solicitud para project_id: {request.project_id}")
    try:
        result = get_recommendations(request.project_id, request.user_query)

        if isinstance(result, RagResponse):
            # Si el resultado es del tipo esperado, FastAPI lo serializará correctamente
            return result
        elif isinstance(result, dict) and 'error' in result:
             # Si es un diccionario de error de nuestra lógica RAG
             print(f"Error procesando la solicitud: {result['error']}")
             # Lanza una excepción HTTP que FastAPI convertirá en una respuesta de error
             raise HTTPException(status_code=500, detail=f"Error interno del servidor: {result['error']}")
        else:
             # Caso inesperado
             print(f"Tipo de resultado inesperado: {type(result)}")
             raise HTTPException(status_code=500, detail="Error interno inesperado al procesar la solicitud.")

    except HTTPException as http_exc:
         # Re-lanzar excepciones HTTP para que FastAPI las maneje
         raise http_exc
    except ValueError as ve:
         # Errores específicos como "Proyecto no encontrado"
         raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        # Captura cualquier otra excepción inesperada
        import traceback
        print(f"Excepción no controlada en el endpoint: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fatal en el servidor: {e}")

# --- Endpoint de Health Check (Buena práctica) ---
@app.get("/health", summary="Verifica el estado de la API")
async def health_check():
    # Podrías añadir más checks aquí (ej. si la DB vectorial responde)
    return {"status": "ok"}

# --- Ejecución para Desarrollo Local ---
if __name__ == "__main__":
    print("Ejecutando servidor FastAPI en modo desarrollo...")
    # host="0.0.0.0" permite conexiones desde otras máquinas en la red local
    # reload=True reinicia automáticamente el servidor cuando detecta cambios en el código
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)