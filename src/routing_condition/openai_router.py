from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import List
from src.routing_condition.i_router import IRouter

class OpenAIRouter(IRouter):
    def __init__(self, model: str = "gpt-4o"):
        load_dotenv()
        self.model = model
        self.client = OpenAI(
        # This is the default and can be omitted
            api_key=os.getenv('OPENAI_API_KEY'),
        )

    def get_response(self, prompt: str) -> str:
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
    