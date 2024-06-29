from dotenv import load_dotenv
import os
from openai import OpenAI
from src.condition.i_condition import ICondition


class OpenAILLM(ICondition):
    def __init__(self, model: str = "gpt-4o"):
        super().__init__()
        # Load .env file if it exists (for local development)
        if os.path.exists('.env'):
            load_dotenv()
        self.model = model
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.getenv("OPENAI_API_KEY"),
        )

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
