from src.condition.builder.code_condition_builder import CodeConditionBuilder
from src.factory.i_object_factory import IObjectFactory
from src.factory.llm_provider import LLMProvider


class ConditionProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.llm_provider = LLMProvider()
        self.register_builder("code", CodeConditionBuilder())

    def get(self, key, **kwargs):
        builder = self.get_builder(key)
        if isinstance(CodeConditionBuilder, builder):
            llm = self.llm_provider.get(key)
            return builder(llm)
