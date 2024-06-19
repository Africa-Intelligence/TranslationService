#https://github.com/ollama/ollama-python?tab=readme-ov-file
import ollama
from src.routing_condition.i_router import IRouter

class OllamaRouter(IRouter):
    def __init__(self, model: str = "llama3"):
        self.model = model

    def get_response(self, prompt: str) -> str:
        response = ollama.chat(model=self.model, messages=[
            {
            'role': 'user',
            'content': prompt,
            },
        ])

        return response['message']['content']
    