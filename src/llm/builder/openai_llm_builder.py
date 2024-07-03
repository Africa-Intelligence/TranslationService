from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_builder import IBuilder
from src.llm.openai_llm import OpenAILLM


class OpenAILLMBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, environment: IEnvironment):
        if not self._instance:
            openai_api_key = environment.get_value(EnvVar.OpenAIAPIKey.value)
            self._instance = OpenAILLM(openai_api_key)
        return self._instance
