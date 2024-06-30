from src.condition.code_condition import CodeCondition
from src.llm.i_llm import ILLM


class CodeConditionBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, llm: ILLM, **_ignored):
        if not self._instance:
            self._instance = CodeCondition(llm)
        return self._instance
