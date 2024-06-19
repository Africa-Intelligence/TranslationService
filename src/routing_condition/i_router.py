import pandas as pd

class IRouter(object):
    def __init__(self):
        pass

    def get_response(self, prompt: str) -> str:
        pass
    
    def is_code(self, row: pd.DataFrame) -> str:
        """
        Returns Yes if the text contains code and No if it does not.
        """
        text = row.str.cat(sep='\n')
        prompt = f"""
            I need you to analyze a question answer sequence of text and determine whether it contains code written 
            in any programming language. Please respond with "Yes" if the text contains code and 
            "No" if it does not. All langauages are valid, including markup languages.
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
        answer = self.get_response(prompt)
        return answer