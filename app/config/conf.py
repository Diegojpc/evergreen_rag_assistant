from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Config(BaseSettings):
    API_NAME: str = "AVA AI - Asistente Virtual en Agronomía"
    API_DESCRIPTION: str = (
        "API para obtener recomendaciones de cultivos y prácticas agrícolas"
    )
    API_VERSION: str = "1.0.0"

    HF_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr


config = Config()
