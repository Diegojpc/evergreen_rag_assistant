import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from pydantic import BaseModel, Field
from typing import List, Optional

from config import OPENAI_API_KEY
from knowledge_base import query_knowledge_base
from data_adapters import (
    get_weather_forecast,
    get_sensor_data,
    get_recent_images_analysis,
    get_lunar_phase,
    get_project_details
)

# --- Definición del Modelo de Salida Esperado ---
# Usamos Pydantic para definir la estructura JSON que queremos que el LLM genere
class RecommendationItem(BaseModel):
    action: str = Field(description="Tarea específica recomendada (ej. 'Regar', 'Aplicar fertilizante NPK', 'Monitorear Mosca Blanca').")
    details: str = Field(description="Detalles concretos de la acción (ej. '15 L/m²', 'NPK 10-20-10 a 50 kg/ha', 'Revisar trampas amarillas').")
    priority: str = Field(description="Prioridad de la tarea (ej. 'Alta', 'Media', 'Baja').")
    justification: str = Field(description="Explicación breve basada en datos o conocimiento (ej. 'Humedad suelo baja', 'Fase de floración', 'Pronóstico favorable para plaga').")

class EarlyWarning(BaseModel):
    risk_type: str = Field(description="Tipo de riesgo detectado (ej. 'Mildiu', 'Estrés Hídrico', 'Helada Leve', 'Pulgón').")
    level: str = Field(description="Nivel de riesgo (ej. 'Alto', 'Medio', 'Bajo', 'Potencial').")
    trigger_factor: str = Field(description="Factor principal que causa el riesgo (ej. 'Alta humedad y T nocturna > 15°C', 'Baja humedad suelo', 'Pronóstico T < 2°C', 'Detectado en análisis de imagen').")
    preventive_measure: Optional[str] = Field(description="Sugerencia de medida preventiva o de monitoreo.", default=None)

class RagResponse(BaseModel):
    project_id: str = Field(description="Identificador del proyecto para el cual es la recomendación.")
    parcela_id: str = Field(description="Identificador de la parcela.")
    current_summary: str = Field(description="Resumen muy breve de la situación actual del cultivo.")
    recommendations: List[RecommendationItem] = Field(description="Lista de acciones recomendadas y priorizadas.")
    warnings: List[EarlyWarning] = Field(description="Lista de alertas tempranas sobre riesgos potenciales.")
    # optional_impact_estimation: Optional[str] = Field(description="Estimación cualitativa del impacto (opcional)", default=None)


# --- Configuración del LLM y Parser ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, openai_api_key=OPENAI_API_KEY)
# Usaremos un parser JSON para obtener una salida estructurada
output_parser = JsonOutputParser(pydantic_object=RagResponse)

# --- Plantilla del Prompt ---
# Esta es la parte más importante para guiar al LLM
system_template = """
Eres un Asistente Agrónomo experto virtual para el sistema Evergreen. Tu objetivo es proporcionar recomendaciones
contextualizadas, proactivas y basadas en evidencia para la gestión de cultivos.

Utiliza la siguiente información contextual para generar tu respuesta:
1.  **Detalles del Cultivo/Proyecto:** {project_details}
2.  **Datos de Sensores (si disponibles):** {sensor_data}
3.  **Análisis de Imágenes Recientes (si disponible):** {image_analysis}
4.  **Pronóstico del Clima:** {weather_forecast}
5.  **Fase Lunar (contexto adicional opcional):** {lunar_phase}
6.  **Conocimiento Agronómico Recuperado (manuales, historial, mejores prácticas):**
    {retrieved_knowledge}

Basándote en TODA esta información y la pregunta o solicitud del usuario, genera una respuesta estructurada.
La respuesta DEBE seguir estrictamente el siguiente formato JSON:
{format_instructions}

Instrucciones Clave para tu Respuesta:
- Prioriza las acciones más urgentes o impactantes.
- Sé conciso pero claro en las recomendaciones y justificaciones.
- Basa tus justificaciones explícitamente en los datos proporcionados (sensores, clima, imágenes, historial, manuales). Menciona la fuente si es relevante (ej. 'según manual', 'debido a pronóstico').
- Si detectas riesgos (plagas, enfermedades, clima adverso), inclúyelos en la sección 'warnings'.
- Si no hay datos de sensores o imágenes, indícalo y basa tus recomendaciones en el resto de la información.
- Si la pregunta es muy general (ej. '¿qué hacer?'), enfócate en las próximas acciones clave para la fase actual del cultivo y las condiciones.
- El horizonte temporal por defecto es la próxima semana, a menos que la pregunta especifique otro.
"""

human_template = "Solicitud del Usuario/Sistema: {user_query}"

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ],
    input_variables=["project_details", "sensor_data", "image_analysis", "weather_forecast", "lunar_phase", "retrieved_knowledge", "user_query"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()} # Inyecta las instrucciones de formato JSON
)

# --- Función para Formatear Datos de Entrada ---
def format_context_data(project_id: str, user_query: str) -> dict:
    """Recopila y formatea todos los datos necesarios para el prompt."""
    project_details = get_project_details(project_id)
    if not project_details:
        raise ValueError(f"Proyecto {project_id} no encontrado.")

    parcela_id = project_details.get("parcela_id", "Desconocida")
    location = f"Parcela {parcela_id}" # Simplificado, podría ser más específico

    # Usar 'N/A' o mensajes claros si los datos no están disponibles
    sensor_data = get_sensor_data(parcela_id) or "No disponibles"
    image_analysis = get_recent_images_analysis(parcela_id) or "No disponible"
    weather_forecast = get_weather_forecast(location) or "No disponible"
    lunar_phase = get_lunar_phase() or "No disponible"

    # Crear un contexto combinado para la búsqueda en la base de conocimiento
    # Incluimos detalles clave del cultivo y la consulta
    knowledge_query = f"Cultivo: {project_details.get('crop_type', '')}, Fase: {project_details.get('current_phase', '')}. Historial Parcela: {parcela_id}. Consulta: {user_query}"
    retrieved_knowledge_list = query_knowledge_base(knowledge_query)
    # Formatear conocimiento recuperado como una lista de strings o un solo bloque
    retrieved_knowledge = "\n---\n".join(retrieved_knowledge_list) if retrieved_knowledge_list else "No se encontró información específica relevante en la base de conocimiento."

    return {
        "project_details": json.dumps(project_details, indent=2),
        "sensor_data": json.dumps(sensor_data, indent=2) if isinstance(sensor_data, dict) else sensor_data,
        "image_analysis": json.dumps(image_analysis, indent=2) if isinstance(image_analysis, dict) else image_analysis,
        "weather_forecast": json.dumps(weather_forecast, indent=2) if isinstance(weather_forecast, dict) else weather_forecast,
        "lunar_phase": json.dumps(lunar_phase, indent=2) if isinstance(lunar_phase, dict) else lunar_phase,
        "retrieved_knowledge": retrieved_knowledge,
        "user_query": user_query,
        # Pasar IDs para incluirlos en la respuesta final si es necesario
        "project_id_passthrough": project_id,
        "parcela_id_passthrough": parcela_id
    }

# --- Creación de la Cadena RAG (Runnable) con LCEL ---
# Usamos RunnableParallel para preparar las entradas del prompt
# Usamos RunnablePassthrough para pasar datos directamente al siguiente paso si es necesario

rag_chain = (
    # 1. Recopilar y formatear datos en paralelo (o secuencial si hay dependencias)
    RunnableParallel(
        context_data=RunnablePassthrough(), # La entrada inicial es el dict con project_id y user_query
        # Pasamos directamente los IDs para que estén disponibles al final si los necesitamos fuera del contexto del LLM
        project_id=lambda x: x["project_id_passthrough"],
        parcela_id=lambda x: x["parcela_id_passthrough"]
    )
    |
    # 2. Construir el prompt con los datos formateados
    RunnableParallel(
        llm_input=lambda x: prompt.invoke(x['context_data']), # Llama al prompt con los datos formateados
        project_id=lambda x: x['project_id'], # Pasa el project_id
        parcela_id=lambda x: x['parcela_id'] # Pasa el parcela_id
    )
    |
    # 3. Llamar al LLM con el prompt generado
    RunnableParallel(
        llm_output=lambda x: llm.invoke(x['llm_input']), # Llama al LLM
        project_id=lambda x: x['project_id'], # Pasa el project_id
        parcela_id=lambda x: x['parcela_id'] # Pasa el parcela_id
    )
   |
    # 4. Parsear la salida del LLM usando nuestro Pydantic model
    RunnableParallel(
        parsed_response=lambda x: output_parser.invoke(x['llm_output']), # Parsea la respuesta JSON
        project_id=lambda x: x['project_id'], # Pasa el project_id
        parcela_id=lambda x: x['parcela_id'] # Pasa el parcela_id
    )
    |
    # 5. (Opcional) Paso final para asegurar que los IDs estén en el objeto final si el LLM no los incluyó correctamente
    #    Aunque le pedimos al LLM que los incluya, esto es una salvaguarda.
     (lambda x: 
        RagResponse(
            project_id=x['project_id'],
            parcela_id=x['parcela_id'],
            current_summary=x['parsed_response'].get('current_summary', ''),
            recommendations=x['parsed_response'].get('recommendations', []),
            warnings=x['parsed_response'].get('warnings', [])
        )
    )
)


def get_recommendations(project_id: str, user_query: str) -> RagResponse | dict:
    """Función principal para obtener recomendaciones."""
    try:
        print(f"\n--- Iniciando Proceso RAG para Proyecto: {project_id} ---")
        print(f"Consulta: {user_query}")

        # Formatea los datos de entrada
        input_data = format_context_data(project_id, user_query)

        # Ejecuta la cadena RAG
        print("Invocando la cadena RAG con el LLM...")
        result = rag_chain.invoke(input_data)
        print("Respuesta recibida y parseada.")

        # Devuelve el objeto Pydantic parseado
        return result

    except ValueError as ve:
         print(f"Error de Valor: {ve}")
         return {"error": str(ve)}
    except Exception as e:
        import traceback
        print(f"Error inesperado en el proceso RAG: {e}")
        print(traceback.format_exc()) # Imprime el traceback completo para depuración
        return {"error": f"Ocurrió un error inesperado: {e}"}

if __name__ == "__main__":
    # Ejemplo de uso directo (para probar)
    from knowledge_base import initialize_knowledge_base
    initialize_knowledge_base() # Asegúrate de que la DB esté lista

    test_project_id = "PROJ_TOMATE_2024_P123"
    # test_query = "¿Qué debo hacer esta semana con mis tomates?"
    test_query = "¿Qué debo hacer esta semana con mis tomates?"

    recommendation_result = get_recommendations(test_project_id, test_query)

    print("\n--- Resultado Final RAG ---")
    if isinstance(recommendation_result, RagResponse):
         # Usamos .dict() o .model_dump() en Pydantic v2 para imprimir bonito
         print(json.dumps(recommendation_result.model_dump(), indent=2))
    else:
         print(recommendation_result) # Imprime el diccionario de error