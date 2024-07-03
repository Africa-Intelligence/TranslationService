from src.condition.min_chars_condition import MinCharsCondition
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_builder import IBuilder


class MinCharsConditionBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, environment: IEnvironment):
        if not self._instance:
            min_char_length = environment.get_value(EnvVar.MinCharLength.value)
            self._instance = MinCharsCondition(int(min_char_length))
        return self._instance
