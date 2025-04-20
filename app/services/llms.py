from pydantic import BaseModel
from huggingface_hub import InferenceClient
from openai import OpenAI

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
            temperature=0.7,
        )

    def query_openai_model(
        self, model: ImplementedModels, system_prompt: str, user_prompt: str
    ) -> str:
        completion = OpenAI(
            api_key=config.OPENAI_API_KEY.get_secret_value()
        ).chat.completions.create(
            model=model.value,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        response_content = completion.choices[0].message.content

        if response_content:
            return response_content.strip()
        else:
            raise Exception("Model returned empty content.")
