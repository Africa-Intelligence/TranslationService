from src.condition.builder.code_condition_builder import CodeConditionBuilder
from src.factory.i_object_factory import IObjectFactory


class ConditionProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.register_builder("code", CodeConditionBuilder())
