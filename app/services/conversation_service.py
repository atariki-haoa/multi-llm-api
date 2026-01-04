from typing import Dict, Any, Optional
from app.services.redis_service import (
    create_conversation,
    get_conversation_history,
    save_message
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ConversationService:
    def get_or_create(
        self,
        conversation_id: Optional[str],
        model_name: str,
        message: str
    ) -> Dict[str, Any]:
        if not conversation_id:
            conversation = create_conversation(model_name, message)
            if not conversation:
                logger.error('Error al crear conversación')
                raise ValueError('Error al crear conversación')
            logger.info(f'Nueva conversación creada: {conversation["conversation_id"]}')
            return conversation
        else:
            conversation = get_conversation_history(conversation_id)
            if not conversation.get('messages'):
                conversation['messages'] = []
            if not conversation.get('model'):
                conversation['model'] = model_name
            
            conversation['messages'].append({
                'role': 'user',
                'content': message
            })
            conversation['conversation_id'] = conversation_id
            logger.debug(f'Mensaje añadido a conversación existente: {conversation_id}')
            return conversation
    
    def save_response(self, conversation: Dict[str, Any], response_text: str) -> bool:
        if response_text:
            conversation['messages'].append({
                'role': 'model',
                'content': response_text
            })
        
        success = save_message(conversation)
        if success:
            logger.debug(f'Respuesta guardada en conversación: {conversation["conversation_id"]}')
        else:
            logger.warning(f'Error al guardar respuesta en conversación: {conversation.get("conversation_id")}')
        return success
    
    def get_history(self, conversation_id: str) -> Dict[str, Any]:
        return get_conversation_history(conversation_id)
