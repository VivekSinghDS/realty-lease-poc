
from enum import Enum
from typing import Any, Dict
from adapters.llms.base import LargeLanguageModel
from anthropic import Anthropic, MessageStream
import os 

class CLAUDE_CONFIG(Enum):
    MAX_TOKENS = 15000
    TOP_K = 250
    STOP_SEQUENCES = []
    TEMPERATURE = 0
    TOP_P = 0.999
    MODEL_ID = "claude-3-7-sonnet-20250219"
    
    
class AnthropicAdapter(LargeLanguageModel):
    
    def __init__(self):
        """
        Initialize the Anthropic client with API key.
        
        Args:
            batch_size: Not used in this implementation but kept for interface compatibility
            prefix: Not used in this implementation but kept for interface compatibility
        """
        self.anthropic_client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    
    def get_streaming_response(self, payload: Dict[str, Any]):
        """
        Make a streaming call to Anthropic API.
        
        Args:
            payload: Dictionary containing the request parameters for the model
            
        Returns:
            Response object from Anthropic with streaming capability
            
        Raises:
            Exception: If there's an issue with the request
        """
        try:
            # user = payload['user_prompt']
            # system = payload['system']
            system = 'you are a helpful assistant'
            user = [{"role": "user", "content": "hi"}]
            response = self.anthropic_client.messages.stream(
                model = CLAUDE_CONFIG.MODEL_ID.value,
                system = system,
                messages = user,
                max_tokens=CLAUDE_CONFIG.MAX_TOKENS.value,
                temperature=CLAUDE_CONFIG.TEMPERATURE.value,
                top_k=CLAUDE_CONFIG.TOP_K.value,
                top_p=CLAUDE_CONFIG.TOP_P.value, 
            )
            stream = response.__enter__()   # manually enter context
            return stream            
        except Exception as e:
            raise e
    
    def process_response(self, response: MessageStream):
        for text in response:
            if text.type == "content_block_delta":
                yield text.delta.text   
    
    def get_payload(self, system_prompt, user_prompt):
        return {
            "system": system_prompt, 
            "user_prompt": user_prompt
        } 
         
    def get_non_streaming_response(self, payload: Dict[str, Any]) -> str:
        """
        Make a non-streaming call to Anthropic API.
        
        Args:
            payload: Dictionary containing the request parameters for the model
            
        Returns:
            Dictionary containing the parsed response from Anthropic
            
        Raises:
            Exception: If there's an issue with the request
        """
        try:
            user = payload['user_prompt']
            system = payload['system']
            response = self.anthropic_client.messages.create(
                model = CLAUDE_CONFIG.MODEL_ID.value,
                system = system,
                messages = user,
                max_tokens=CLAUDE_CONFIG.MAX_TOKENS.value,
                temperature=CLAUDE_CONFIG.TEMPERATURE.value,
                top_k=CLAUDE_CONFIG.TOP_K.value,
                top_p=CLAUDE_CONFIG.TOP_P.value, 
            )
            return response.content[0].text
            
        except Exception as e:
            raise e

anthropic = AnthropicAdapter()
# anthropic.stream({"role": "user", "content": "hi"})