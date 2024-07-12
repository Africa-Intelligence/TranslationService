from typing import List, Dict
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.api.translation.i_translate_api import ITranslateAPI
from src.api.translation.translation_result import TranslationResult


def _combine_translation_chunks(translations: List[str], chunks_per_entry: List[int]):
    combined_translations = []
    running_index = 0
    for num_chunks in chunks_per_entry:
        translation_chunks = translations[running_index: running_index+num_chunks]
        combined_translations.append(''.join(translation_chunks))
        running_index += num_chunks
    return combined_translations


class OpenSourceTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str], chunk_size: int):
        super().__init__(from_language, to_languages)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=0,
            length_function=len,
        )

    def translate(
            self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)
        chunks_per_entry: List[int] = []
        all_chunks: List[str] = []
        for entry in flattened_content:
            entry_chunks = self._get_chunks(entry)
            chunks_per_entry.append(len(entry_chunks))
            all_chunks.extend(entry_chunks)

        for to_language in self.to_languages:
            translated_chunks = self._translate(all_chunks, to_language)
            translations = _combine_translation_chunks(translated_chunks, chunks_per_entry)

            translation_data = TranslationResult(
                column_names=column_names,
                positions=positions,
                original_content=flattened_content,
                translated_content=translations,
                from_language=self.from_language,
                to_language=to_language
            )

            translated_df = self._reconstruct_dataframe(translation_data)
            result[to_language] = translated_df

        return result

    def _get_chunks(self, text) -> List[str]:
        chunks: List[Document] = self.text_splitter.create_documents([text])
        return [chunk.page_content for chunk in chunks]

    def _translate(self, batch: List[str], to_language: str) -> List[str]:
        raise NotImplementedError
