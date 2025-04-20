from pydantic import BaseModel
from huggingface_hub import InferenceClient
import openai
import logging

from app.models.llms import ImplementedModels
from app.config.conf import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMsService(BaseModel):
    def _get_openai_client(self) -> openai.OpenAI:
        """Crea y devuelve una nueva instancia del cliente OpenAI."""
        logger.debug("Initializing OpenAI client for this request.")
        # Asegúrate que la clave API se lee correctamente desde la config
        api_key = config.OPENAI_API_KEY.get_secret_value()
        if not api_key:
             logger.error("OpenAI API Key is not configured!")
             # Puedes lanzar un error aquí si prefieres fallar rápido
             raise ValueError("OpenAI API Key not found in configuration.")
        return openai.OpenAI(api_key=api_key)
    
    def query_huggingface_model(self, model: ImplementedModels, prompt: str) -> str:
        """Queries a specified Hugging Face model using the InferenceClient."""
        try:
            logger.info(f"Querying Hugging Face model: {model.value}")
            client: InferenceClient = InferenceClient(
                model=model.value,
                token=config.HF_TOKEN.get_secret_value(),
            )
            response = client.text_generation(
                prompt=prompt,
                max_new_tokens=500, 
                temperature=0.7
            )
            logger.info(f"Received response from Hugging Face model: {model.value}")
            return response
        except Exception as e:
            logger.error(f"Error querying Hugging Face model {model.value}: {e}", exc_info=True)
            raise RuntimeError(f"Failed to query Hugging Face model {model.value}: {e}") from e

    def query_openai_model(self, model: ImplementedModels, system_prompt: str, user_prompt: str) -> str:
        """
        Queries the specified OpenAI model (e.g., gpt-4o) using the official OpenAI client.
        Separates system instructions from the user's specific query.
        """
        if not model.value.startswith("gpt"):
             raise ValueError(f"Model {model.value} is not a supported OpenAI model for this method.")

        try:
            logger.info(f"Querying OpenAI model: {model.value}")
            completion = self._get_openai_client().chat.completions.create(
                model=model.value,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            response_content = completion.choices[0].message.content
            logger.info(f"Received response from OpenAI model: {model.value}")
            if response_content:
                return response_content.strip()
            else:
                logger.warning(f"OpenAI model {model.value} returned empty content.")
                return "El modelo no generó una respuesta."

        except openai.APIConnectionError as e:
            logger.error(f"OpenAI API request failed to connect: {e}", exc_info=True)
            raise RuntimeError(f"Failed to connect to OpenAI API: {e}") from e
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API request exceeded rate limit: {e}", exc_info=True)
            raise RuntimeError(f"OpenAI rate limit exceeded: {e}") from e
        except openai.APIStatusError as e:
            logger.error(f"OpenAI API returned an error status: {e.status_code} - {e.response}", exc_info=True)
            raise RuntimeError(f"OpenAI API error: {e.status_code} - {e.message}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred while querying OpenAI model {model.value}: {e}", exc_info=True)
            raise RuntimeError(f"Failed to query OpenAI model {model.value}: {e}") from e