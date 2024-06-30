from src.llm.ollama_llm import OllamaLLM


class OllamaLLMBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        if not self._instance:
            self._instance = OllamaLLM()
        return self._instance
