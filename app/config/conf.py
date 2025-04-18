from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Config(BaseSettings):
    API_NAME: str = "Evergreen RAG Assistant API"
    API_DESCRIPTION: str = "API to get recommendations for crop management using RAG"
    API_VERSION: str = "1.0.0"

    HF_TOKEN: SecretStr


config = Config()
