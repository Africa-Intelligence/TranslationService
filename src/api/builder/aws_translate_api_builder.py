from src.api.aws_translate_api import AWSTranslateAPI
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_builder import IBuilder


class AWSTranslateAPIBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, env: IEnvironment):
        if not self._instance:
            from_language = env.get_value(EnvVar.FromLanguage.value)
            to_languages = env.get_value(EnvVar.ToLanguages.value)
            aws_access_key = env.get_value(EnvVar.AWSAccessKey.value)
            aws_secret_key = env.get_value(EnvVar.AwsSecretKey.value)
            aws_session_token = env.get_value(EnvVar.AWSSessionToken.value)
            aws_region = env.get_value(EnvVar.AWSRegion.value)
            self._instance = AWSTranslateAPI(
                from_language, to_languages, aws_access_key, aws_secret_key, aws_session_token, aws_region
            )
        return self._instance
