from src.api.translation.builder.aws_translate_api_builder import AWSTranslateAPIBuilder
from src.api.translation.builder.azure_translate_api_builder import AzureTranslateAPIBuilder
from src.api.translation.builder.meta_translate_api_builder import MetaTranslateAPIBuilder
from src.api.translation.builder.opus_translate_api_builder import OpusTranslateAPIBuilder
from src.factory.i_object_factory import IObjectFactory


class TranslateAPIProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.register_builder("aws", AWSTranslateAPIBuilder())
        self.register_builder("azure", AzureTranslateAPIBuilder())
        self.register_builder("opus", OpusTranslateAPIBuilder())
        self.register_builder("meta", MetaTranslateAPIBuilder())
