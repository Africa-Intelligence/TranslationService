from src.environment.i_environment import IEnvironment
from src.factory.i_builder import IBuilder
from src.llm.ollama_llm import OllamaLLM


class OllamaLLMBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, _ignored: IEnvironment):
        if not self._instance:
            self._instance = OllamaLLM()
        return self._instance
