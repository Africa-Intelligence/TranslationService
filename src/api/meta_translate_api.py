import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.api.i_translate_api import ITranslateAPI
from src.client.meta_client import MetaClient
from typing import Dict, List


class MetaTranslateAPI(ITranslateAPI):

    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)
        self.models: Dict[str, MetaClient] = {}
        for to_language in to_languages:
            self.models[to_language] = MetaClient(from_language=from_language, to_language=to_language)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=20,
            length_function=len,
        )

    def translate(self, row: pd.DataFrame, column_names: List[str]) -> Dict[str, pd.DataFrame]:
        result = {str: [pd.DataFrame]}
        for to_language in self.to_languages:
            result[to_language] = pd.DataFrame()

        for to_language in self.to_languages:
            for col_index, column_name in enumerate(column_names):
                original_text = row.iloc[col_index]
                translation = self._translate(original_text, to_language) if original_text != '' else original_text
                result[to_language].at[0, f'{self.from_language}-{column_name}'] = original_text
                result[to_language].at[0, f'{to_language}-{column_name}'] = translation

        return result

    def _translate(self, text: str, to_language: str) -> str:
        result = ""
        chunks = self._get_chunks(text)
        for chunk in chunks:
            translated_chunk = self.models[to_language].translate(chunk)[0]
            result += translated_chunk
        return result

    def _get_chunks(self, text) -> List[str]:
        chunks: List[Document] = self.text_splitter.create_documents([text])
        return [chunk.page_content for chunk in chunks]
