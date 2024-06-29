from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class OpusClient(object):
    def __init__(self, from_language: str, to_language):
        # supported languages - https://huggingface.co/Helsinki-NLP
        model_name = f"Helsinki-NLP/opus-mt-{from_language}-{to_language}"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Check for CUDA, MPS (M1), or fall back to CPU
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        self.model.to(self.device)

    def translate(self, text) -> str:
        encoded_input = self.tokenizer(text, return_tensors="pt", padding=True).to(self.device)
        translated_tokens = self.model.generate(**encoded_input)
        translated_text = self.tokenizer.batch_decode(
            translated_tokens, skip_special_tokens=True
        )[0]
        return translated_text
