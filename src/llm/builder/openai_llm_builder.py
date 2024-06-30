from src.llm.openai_llm import OpenAILLM


class OpenAILLMBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, open_api_key: str, **kwargs):
        if not self._instance:
            self._instance = OpenAILLM(open_api_key)
        return self._instance
