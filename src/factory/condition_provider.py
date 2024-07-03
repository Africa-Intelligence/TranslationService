from src.condition.builder.code_condition_builder import CodeConditionBuilder
from src.condition.builder.min_chars_condition_builder import MinCharsConditionBuilder
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_object_factory import IObjectFactory
from src.factory.llm_provider import LLMProvider


class ConditionProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.llm_provider = LLMProvider()
        self.register_builder("code", CodeConditionBuilder())
        self.register_builder("min_chars", MinCharsConditionBuilder())

    def get(self, key, environment: IEnvironment):
        builder = self.get_builder(key)
        if isinstance(builder, CodeConditionBuilder):
            llm_key = environment.get_value(EnvVar.LLM.value)
            llm = self.llm_provider.get(llm_key, environment)
            return builder(llm)
        elif isinstance(builder, MinCharsConditionBuilder):
            return builder(environment)
        else:
            raise ValueError(key)
