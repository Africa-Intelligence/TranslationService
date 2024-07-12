import unittest
from typing import List

import pandas as pd

from src.api.translation.open_source.open_source_translate_api import _combine_translation_chunks, \
    OpenSourceTranslateAPI


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.FROM_LANGUAGE = "en"
        self.TO_LANGUAGES = ["af"]
        self.CHUNK_SIZE = 100
        self.translations = [
            "The quick brown fox jumps over the lazy dog.",
            "Sphinx of black quartz, judge my vow."
        ]
        self.column_name = "translations"
        self.batch = pd.DataFrame({self.column_name: self.translations})

    def test_chunks_combined_correctly(self):
        translations = [
            "The quick brown fox", " jumps over", " the lazy dog.",
            "Sphinx of black quartz, ", "judge my vow."
        ]
        lengths = [3, 2]
        result = _combine_translation_chunks(translations, lengths)
        self.assertEqual("The quick brown fox jumps over the lazy dog.", result[0])
        self.assertEqual("Sphinx of black quartz, judge my vow.", result[1])

    def test_translate_text(self):
        api = MockOpenSourceApi(self.FROM_LANGUAGE, self.TO_LANGUAGES, self.CHUNK_SIZE)

        results = api.translate(self.batch, [self.column_name])

        for to_language in self.TO_LANGUAGES:
            rows = results[to_language].get(f'{self.FROM_LANGUAGE}-{self.column_name}')
            for index, row in enumerate(rows):
                self.assertEqual(self.translations[index], row)

    def test_multiple_languages(self):
        to_languages = ["af", "zh"]
        api = MockOpenSourceApi(self.FROM_LANGUAGE, to_languages, self.CHUNK_SIZE)

        results = api.translate(self.batch, [self.column_name])

        for to_language in to_languages:
            rows = results[to_language].get(f'{self.FROM_LANGUAGE}-{self.column_name}')
            for index, row in enumerate(rows):
                self.assertEqual(self.translations[index], row)

    def test_multiple_chunks(self):
        api = MockOpenSourceApi(self.FROM_LANGUAGE, self.TO_LANGUAGES, 25)

        results = api.translate(self.batch, [self.column_name])

        for to_language in self.TO_LANGUAGES:
            rows = results[to_language].get(f'{self.FROM_LANGUAGE}-{self.column_name}')
            for index, row in enumerate(rows):
                self.assertEqual(self.translations[index], row)

class MockOpenSourceApi(OpenSourceTranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str], chunk_size: int):
        super().__init__(from_language, to_languages, chunk_size)

    def _translate(self, batch: List[str], to_language: str) -> List[str]:
        return batch


if __name__ == '__main__':
    unittest.main()
