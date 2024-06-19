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
            You are given a question-answer sequence of text. Your task is to determine whether the text contains 
            code written in any programming language, including markup languages. Respond with "Yes" if the text 
            contains code and "No" if it does not. Do not provide any further explanation or justification. You must 
            be able to handle code snippets in any programming language.
            Examples:
            Input:
                def hello_world():
                    print("Hello, world!")
            Output: Yes

            Input:
                In a 16-bit system, the maximum value of an unsigned integer is 65535.
            Output: No

            Input:
            <html>
                <body>
                    <h1>Hello, World!</h1>
                </body>
            </html>
            Output: Yes

            Input:
            SELECT * FROM users WHERE age > 30;
            Output: Yes

            Input:
            The denominator of 1/4 is 4
            Output: No

            Instruction:

            Now, analyze the following text:

            Input:
            {text}
            Output:         
            """
        answer = self.get_response(prompt)
        return answer