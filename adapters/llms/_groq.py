import os

from groq import Groq

from typing import List
from adapters.llms.base import LargeLanguageModel 


class _Groq(LargeLanguageModel):
    def __init__(self, model_name: str = "gpt-5"):
        self.client = Groq(
            # This is the default and can be omitted
            api_key=os.environ.get("GROQ_API_KEY"),
            max_retries=10,
            timeout = 10
        )
        self.model_name = "openai/gpt-oss-20b"
        
    def get_streaming_response(self, payload: List[dict]):
        return self.client.chat.completions.create(
                model=self.model_name,
                messages=payload,
                stream=True,
                temperature = 0,
            ) 
    
    def get_non_streaming_response(self, payload: List[dict]):
        return self.client.chat.completions.create(
                messages=payload,
                model=self.model_name,
                temperature=0,
                max_completion_tokens=50000,
                max_tokens = 50000
            )