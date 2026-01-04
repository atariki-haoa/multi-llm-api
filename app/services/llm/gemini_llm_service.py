from typing import Dict, Any, List
from google import genai
from app.services.llm.base_llm_service import BaseLLMService
from app.adapters.gemini_adapter import GeminiAdapter
from app.utils.consts import GEMINI_INTEGRATION
from app.utils.model_selector import gemini_model_selector
from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiLLMService(BaseLLMService):
    def __init__(self):
        self.adapter = GeminiAdapter()
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = genai.Client()
            logger.debug('Cliente de Gemini inicializado')
        return self._client
    
    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        logger.info('Iniciando chat con Gemini API')
        
        try:
            mapped_messages = self.adapter.map_messages(messages)
            
            interaction = self.client.interactions.create(
                model=gemini_model_selector(),
                input=mapped_messages
            )
            
            logger.info('Respuesta recibida de Gemini API exitosamente')
            mapped_response = self.adapter.map_response(interaction)
            
            return mapped_response
        except Exception as e:
            logger.error(f'Error al llamar a Gemini API: {str(e)}', exc_info=True)
            raise
    
    def supports_integration(self, integration: str) -> bool:
        return integration == GEMINI_INTEGRATION
    
    def get_integration_name(self) -> str:
        return GEMINI_INTEGRATION
