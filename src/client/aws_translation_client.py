import boto3


class AwsTranslateClient(object):

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str, region_name: str):
        self.client = boto3.client(
            "translate",
            use_ssl=True,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
        )

    def translate(self, text: str, from_language: str, to_language: str):
        # supported languages https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html
        result = self.client.translate_text(
            Text=text, SourceLanguageCode=from_language, TargetLanguageCode=to_language
        )
        return result.get("TranslatedText")
