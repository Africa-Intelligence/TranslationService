from src.condition.code_condition import CodeCondition
from src.factory.i_builder import IBuilder
from src.llm.i_llm import ILLM


class CodeConditionBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, llm: ILLM):
        if not self._instance:
            self._instance = CodeCondition(llm)
        return self._instance
