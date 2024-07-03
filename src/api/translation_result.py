from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TranslationResult:
    column_names: List[str]
    positions: List[Tuple[int, str]]
    original_content: List[str]
    translated_content: List[str]
    from_language: str
    to_language: str