import pandas as pd

from src.llm.i_llm import ILLM
from src.condition.i_condition import ICondition


class CodeCondition(ICondition):

    def __init__(self, llm: ILLM):
        self.llm = llm
        self.TRUE_CONDITION = "yes"

    def execute(self, row: pd.DataFrame) -> bool:
        """
        Returns Yes if the text contains code and No if it does not.
        """
        text = row.str.cat(sep="\n")
        prompt = f"""
            I need you to analyze a question answer sequence of text and determine whether it contains code written 
            in any programming language. Please respond with "Yes" if the text contains code and 
            "No" if it does not. All languages are valid, including markup languages.
            Example 1:
                Input: 
                    def hello_world():
                        print("Hello, world!")
                Output:
                    Yes
            Example 2:
                Input:
                    The quick brown fox jumps over the lazy dog.
                Output:
                    No

            It is important that you only answer with "Yes" or "No". No further explanation or justification
            is needed. You should be robust enough to handle code snippets in any programming language.
            Now, analyze the following text:
                Input:
                    {text}
                Output:                
            """
        answer = self.llm.invoke(prompt)
        return True if answer.lower() == self.TRUE_CONDITION else False
