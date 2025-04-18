from pydantic import BaseModel
from huggingface_hub import InferenceClient

from app.models.llms import ImplementedModels
from app.config.conf import config


class LLMsService(BaseModel):
    def query_huggingface_model(self, model: ImplementedModels, prompt: str) -> str:
        client: InferenceClient = InferenceClient(
            model=model.value,
            token=config.HF_TOKEN.get_secret_value(),
        )

        return client.text_generation(
            prompt=prompt,
            max_new_tokens=250,
        )
