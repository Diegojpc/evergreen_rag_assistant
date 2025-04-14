# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") # Descomentar si se usa

if not OPENAI_API_KEY:
    raise ValueError("La clave API de OpenAI no está configurada en el archivo .env")

# Constantes (se pueden mover a otro archivo si crecen mucho)
VECTOR_DB_PATH = "./chroma_db"
KNOWLEDGE_BASE_DIR = "./sample_knowledge"