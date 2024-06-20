# https://github.com/ollama/ollama-python?tab=readme-ov-file
import ollama

from src.llm.i_llm import ILLM


class OllamaLLM(ILLM):
    def __init__(self, model: str = "llama3"):
        super().__init__()
        self.model = model

    def invoke(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response["message"]["content"]
