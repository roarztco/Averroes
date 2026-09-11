from strands.models.ollama import OllamaModel


def get_model():
    return OllamaModel(
        host="http://localhost:11434",
        model_id="qwen3:8b"
    )