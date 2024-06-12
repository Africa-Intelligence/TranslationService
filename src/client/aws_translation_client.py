import os
import boto3
from dotenv import load_dotenv


class AwsTranslateClient(object):

    def __init__(self):
        load_dotenv()
        self.client = boto3.client(
            "translate",
            use_ssl=True,
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN')
        )

    def translate(self, text: str, from_language: str, to_language: str):
        # supported languages https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html
        result = self.client.translate_text(
            Text=text,
            SourceLanguageCode=from_language,
            TargetLanguageCode=to_language
        )
        return result.get('TranslatedText')