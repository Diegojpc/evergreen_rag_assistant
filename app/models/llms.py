from enum import Enum


class ImplementedModels(Enum):
    """
    An enumeration of language models that are implemented and available for use in the system.

    This enum provides a centralized way to reference and manage the different language models
    that can be used throughout the application. Each model is identified by its Hugging Face
    model identifier.
    """

    FLAN_T5_LARGE = "google/flan-t5-large"
    """Google's FLAN-T5 large model, a fine-tuned version of T5 for instruction following."""

    MISTRAL_8X7B = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    """Mistral's Mixtral 8x7B model, a mixture of experts model optimized for instruction following."""
