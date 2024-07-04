from typing import List
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
from transformers import pipeline

class MetaClient(object):
    def __init__(self):
        # supported languages - https://huggingface.co/facebook/m2m100_418M
        model_name = "facebook/m2m100_418M"
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_name)
        # Check for CUDA, MPS (M1), or fall back to CPU
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        self.pipe = pipeline(task="translation", model=self.model, tokenizer=self.tokenizer, device=self.device)

    def translate(self, batch: List[str], from_language: str, to_language: str) -> str:
        result = self.pipe(batch, src_lang=from_language, tgt_lang=to_language, batch_size=len(batch))
        return [item['translation_text'] for item in result]
