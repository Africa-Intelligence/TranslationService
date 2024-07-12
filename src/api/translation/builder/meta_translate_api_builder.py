from src.api.translation.open_source.meta_translate_api import MetaTranslateAPI
from src.environment.i_environment import EnvVar, IEnvironment
from src.factory.i_builder import IBuilder


class MetaTranslateAPIBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, env: IEnvironment):
        if not self._instance:
            from_language = env.get_value(EnvVar.FromLanguage.value)
            to_languages = env.get_value(EnvVar.ToLanguages.value)
            chunk_size = env.get_value(EnvVar.ChunkSize.value)
            self._instance = MetaTranslateAPI(from_language, to_languages, int(chunk_size))
        return self._instance
