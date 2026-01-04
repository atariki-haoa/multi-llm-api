from typing import Dict, Any, List
import requests
import os
from app.services.llm.base_llm_service import BaseLLMService
from app.adapters.ngrok_adapter import NgrokAdapter
from app.utils.consts import NGROK_INTEGRATION
from app.utils.model_selector import ngrok_model_selector
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NgrokLLMService(BaseLLMService):
    def __init__(self):
        self.adapter = NgrokAdapter()
        self.base_url = os.environ.get('NGROK_BASE_URL', 'http://localhost:8080')
        self.api_key = os.environ.get('NGROK_API_KEY')
    
    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        logger.info('Iniciando chat con NGROK API')
        
        try:
            mapped_messages = self.adapter.map_messages(messages)
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            payload = {
                'model': ngrok_model_selector(),
                'messages': mapped_messages
            }
            
            response = requests.post(
                f'{self.base_url}/v1/chat/completions',
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            
            logger.info('Respuesta recibida de NGROK API exitosamente')
            mapped_response = self.adapter.map_response(response.json())
            
            return mapped_response
        except requests.exceptions.RequestException as e:
            logger.error(f'Error al llamar a NGROK API: {str(e)}', exc_info=True)
            raise
        except Exception as e:
            logger.error(f'Error inesperado en NGROK service: {str(e)}', exc_info=True)
            raise
    
    def supports_integration(self, integration: str) -> bool:
        return integration == NGROK_INTEGRATION
    
    def get_integration_name(self) -> str:
        return NGROK_INTEGRATION
