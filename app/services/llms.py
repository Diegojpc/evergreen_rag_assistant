from pydantic import BaseModel
from huggingface_hub import InferenceClient

from app.models.llms import ImplementedModels
from app.config.conf import config


class LLMsService(BaseModel):
    """
    A service class for interacting with various language models through the Hugging Face Hub.

    This service provides methods to query different language models that are implemented
    in the system. It handles the connection and authentication with the Hugging Face Hub
    and provides a standardized interface for text generation.
    """

    def query_huggingface_model(self, model: ImplementedModels, prompt: str) -> str:
        """
        Query a specified language model from Hugging Face Hub with a given prompt.

        Args:
            model (ImplementedModels): The language model to use for text generation.
                                     Must be one of the implemented models in the system.
            prompt (str): The input text prompt to send to the model.

        Returns:
            str: The generated text response from the model.

        Note:
            The function uses the Hugging Face Hub API token from the configuration
            for authentication. The response is limited to 250 new tokens by default.
        """

        client: InferenceClient = InferenceClient(
            model=model.value,
            token=config.HF_TOKEN.get_secret_value(),
        )

        return client.text_generation(
            prompt=prompt,
            max_new_tokens=250,
        )
