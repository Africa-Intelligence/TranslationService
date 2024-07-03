from src.factory.i_object_factory import IObjectFactory
from src.llm.builder.ollama_llm_builder import OllamaLLMBuilder
from src.llm.builder.openai_llm_builder import OpenAILLMBuilder


class LLMProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.register_builder("ollama", OllamaLLMBuilder())
        self.register_builder("openai", OpenAILLMBuilder())
