"""LLM Service for connecting to various LLM providers."""
from typing import Optional, List, Dict
import openai
from app.config import settings


class LLMService:
    """Service for interacting with LLM providers."""
    
    def __init__(self):
        """Initialize the LLM service based on configuration."""
        self.provider = settings.llm_provider.lower()
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
            openai.api_key = settings.openai_api_key
            self.client = openai
            self.model = settings.openai_model
            
        elif self.provider == "azure":
            if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
                raise ValueError("Azure OpenAI endpoint and API key are required")
            openai.api_type = "azure"
            openai.api_key = settings.azure_openai_api_key
            openai.api_base = settings.azure_openai_endpoint
            openai.api_version = settings.azure_openai_api_version
            self.client = openai
            self.model = settings.azure_openai_deployment_name
            
        elif self.provider == "openai-compatible":
            # For compatible APIs like Ollama, LocalAI, etc.
            base_url = settings.azure_openai_endpoint or "http://localhost:11434/v1"
            openai.api_base = base_url
            openai.api_key = settings.azure_openai_api_key or "ollama"
            self.client = openai
            self.model = settings.openai_model
            
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def generate_response(self, messages: List[Dict[str, str]], 
                               temperature: float = 0.7, 
                               max_tokens: Optional[int] = None) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            # Use async client if available, otherwise run in executor
            import asyncio
            loop = asyncio.get_event_loop()
            
            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature
            }
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Run the synchronous call in executor to avoid blocking
            # OpenAI SDK 0.27.x uses ChatCompletion.create
            response = await loop.run_in_executor(
                None,
                lambda: self.client.ChatCompletion.create(**request_params)
            )
            
            # Extract only the response content, no metadata
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")
    
    def get_provider_info(self) -> Dict:
        """Get information about the current LLM provider (for debugging, not exposed to UI)."""
        return {
            "provider": self.provider,
            "model": self.model
        }

