from typing import List
from adapters.llms.base import LargeLanguageModel 
from openai import OpenAI
from utils.schemas import LeaseDocument
import json 



class _OpenAI(LargeLanguageModel):
    def __init__(self, model_name: str = "gpt-5"):
        self.client = OpenAI()
        self.model_name = model_name
        
    def get_streaming_response(self, payload: List[dict]):
        print('inside this method')
        return self.client.responses.create(
            model="gpt-5-nano",
            input=payload,
            stream=True,
            # temperature = 0,
        )
    
    def get_non_streaming_response(self, payload: List[dict]):
        return self.client.responses.create(
            model=self.model_name,
            input=payload,
            max_output_tokens=19999,
        
        ) 