from openai import OpenAI
from src.llm.i_llm import ILLM


class OpenAILLM(ILLM):
    def __init__(self, open_api_key: str, model: str = "gpt-4o"):
        super().__init__()
        self.model = model
        self.client = OpenAI(api_key=open_api_key)

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return response.choices[0].message.content
