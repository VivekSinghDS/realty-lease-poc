from typing import List
from adapters.llms.base import LargeLanguageModel 


class _Perplexity(LargeLanguageModel):
    def __init__(self):
        pass 
    
    def get_streaming_response(self, payload: List[dict]):
        pass 
    
    def get_non_streaming_response(self, payload: List[dict]):
        pass 