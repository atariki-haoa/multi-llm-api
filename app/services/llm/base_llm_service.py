from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMService(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def supports_integration(self, integration: str) -> bool:
        pass
    
    @abstractmethod
    def get_integration_name(self) -> str:
        pass
