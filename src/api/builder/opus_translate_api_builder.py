from src.api.open_source.opus_translate_api import OpusTranslateAPI
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_builder import IBuilder


class OpusTranslateAPIBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, env: IEnvironment):
        if not self._instance:
            from_language = env.get_value(EnvVar.FromLanguage.value)
            to_languages = env.get_value(EnvVar.ToLanguages.value)
            self._instance = OpusTranslateAPI(from_language, to_languages)
        return self._instance
