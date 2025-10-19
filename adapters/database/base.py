import os 
import json 
from abc import ABC, abstractmethod
from typing import List


class Database(ABC):
    @abstractmethod
    def create(self, query: dict):
        pass 
    
    @abstractmethod
    def get(self):
        pass 
    
    @abstractmethod
    def get_single(self, query: dict):
        pass 
    
    @abstractmethod
    def update(self, query: dict):
        pass 
    
    @abstractmethod
    def delete(self, query: dict):
        pass 
    
    
