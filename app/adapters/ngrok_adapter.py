from typing import Dict, Any, List
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NgrokAdapter:
    @staticmethod
    def map_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return messages
    
    @staticmethod
    def map_response(response: Any) -> Dict[str, Any]:
        mapped_response = {
            'text': None,
            'content': None,
            'model': None,
            'usage': {},
            'finish_reason': None
        }
        
        try:
            if isinstance(response, dict):
                mapped_response['text'] = response.get('text') or response.get('content')
                mapped_response['model'] = response.get('model')
                mapped_response['usage'] = response.get('usage', {})
                mapped_response['finish_reason'] = response.get('finish_reason')
            else:
                logger.warning('Respuesta de NGROK en formato no esperado')
        except Exception as e:
            logger.warning(f'Error al mapear respuesta de NGROK: {str(e)}')
        
        return mapped_response
