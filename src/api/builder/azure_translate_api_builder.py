from src.api.azure_translate_api import AzureTranslateAPI
from src.environment.i_environment import EnvVar, IEnvironment
from src.factory.i_builder import IBuilder


class AzureTranslateAPIBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, env: IEnvironment):
        if not self._instance:
            from_language = env.get_value(EnvVar.FromLanguage.value)
            to_languages = env.get_value(EnvVar.ToLanguages.value)
            azure_translate_api_key = env.get_value(EnvVar.AzureTranslateApiKey.value)
            azure_translate_region = env.get_value(EnvVar.AzureTranslateRegion.value)
            self._instance = AzureTranslateAPI(
                from_language, to_languages, azure_translate_api_key, azure_translate_region
            )
        return self._instance
