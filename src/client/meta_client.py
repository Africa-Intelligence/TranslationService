from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class MetaClient(object):
    def __init__(self):
        # supported languages - https://huggingface.co/facebook/m2m100_418M
        model_name = "facebook/m2m100_418M"
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_name)

    def translate(self, text, from_language: str, to_language: str) -> str:
        self.tokenizer.src_lang = from_language
        encoded_input = self.tokenizer(text, return_tensors="pt", padding=True)
        generated_tokens = self.model.generate(
            **encoded_input, forced_bos_token_id=self.tokenizer.get_lang_id(to_language)
        )
        translated_text = self.tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True
        )
        return translated_text
