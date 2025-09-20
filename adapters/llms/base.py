import os 
import json 
from abc import ABC, abstractmethod
from typing import List


class LargeLanguageModel(ABC):
    @abstractmethod
    def get_streaming_response(self, payload: List[dict]):
        pass 
    
    @abstractmethod
    def get_non_streaming_response(self, payload: List[dict]):
        pass 
    
    

