from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class MetaClient(object):
    def __init__(self, from_language: str, to_language):
        # supported languages - https://huggingface.co/Helsinki-NLP
        model_name = "facebook/m2m100_418M"
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_name)
        self.to_language = to_language
        self.from_language = from_language

    def translate(self, text) -> str:
        self.tokenizer.src_lang = self.from_language
        encoded_input = self.tokenizer(text, return_tensors="pt", padding=True)
        generated_tokens = self.model.generate(**encoded_input, forced_bos_token_id=self.tokenizer.get_lang_id(self.to_language))
        translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text
