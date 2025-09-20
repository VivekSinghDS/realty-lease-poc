from typing import List
from adapters.llms.base import LargeLanguageModel 
from openai import OpenAI



class _OpenAI(LargeLanguageModel):
    def __init__(self, model_name: str = "gpt-5"):
        self.client = OpenAI()
        self.model_name = model_name
        
    def get_streaming_response(self, payload: List[dict]):
        pass 
    
    def get_non_streaming_response(self, payload: List[dict]):
        return self.client.responses.create(
            model=self.model_name,
            input=payload
        ) 