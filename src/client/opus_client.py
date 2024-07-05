from typing import List

from transformers import pipeline
import torch


class OpusClient(object):
    def __init__(self, from_language: str, to_language):
        # supported languages - https://huggingface.co/Helsinki-NLP
        model_name = f"Helsinki-NLP/opus-mt-{from_language}-{to_language}"
        # Check for CUDA, MPS (M1), or fall back to CPU
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        self.pipe = pipeline(task="translation", model=model_name, device=self.device)

    def translate(self, batch: List[str]) -> List[str]:
        result = self.pipe(batch, batch_size=len(batch))
        translations = [item['translation_text'] for item in result]
        return translations
