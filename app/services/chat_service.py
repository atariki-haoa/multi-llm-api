from flask import current_app
from app.services.gemini_service import chat_gemini
from app.services.redis_service import create_conversation, get_conversation_history, save_message
from app.models.llm import LLM
from app.models.usage import Usage
from app.models.base import db
from app.utils.logger import get_logger
from app.utils.consts import GEMINI_INTEGRATION, NGROK_INTEGRATION
from typing import Dict, Any, Optional

logger = get_logger(__name__)

def chat_selector():
    with current_app.app_context():
        llms_with_usage = db.session.query(LLM, Usage).join(
            Usage, LLM.id == Usage.llm_id
        ).filter(
            Usage.rpd_count < LLM.rpd
        ).order_by(LLM.priority.asc()).all()
        
        if not llms_with_usage:
            logger.warning('No hay LLMs disponibles (todos han excedido su límite rpd), seleccionando el de menor prioridad')
            llms_with_usage = db.session.query(LLM, Usage).join(
                Usage, LLM.id == Usage.llm_id
            ).order_by(LLM.priority.asc()).all()
        
        if not llms_with_usage:
            logger.error('No hay LLMs configurados en la base de datos')
            raise ValueError('No hay LLMs disponibles en la base de datos')
        
        selected_llm, usage = llms_with_usage[0]
        logger.info(f'LLM seleccionado: {selected_llm.name} (priority: {selected_llm.priority}, rpd_count: {usage.rpd_count}/{selected_llm.rpd})')
        
        return selected_llm
    
def chat(message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    logger.info(f'Iniciando chat - conversation_id: {conversation_id}')
    
    selected_llm = chat_selector()
    
    conversation = {}
    if not conversation_id:
        conversation = create_conversation(selected_llm.name, message)
        if not conversation:
            raise ValueError('Error al crear conversación')
        conversation_id = conversation['conversation_id']
    else:
        conversation = get_conversation_history(conversation_id)
        if not conversation.get('messages'):
            conversation['messages'] = []
        if not conversation.get('model'):
            conversation['model'] = selected_llm.name
        
        conversation['messages'].append({
            'role': 'user',
            'content': message
        })
        conversation['conversation_id'] = conversation_id
    
    response_data = {}
    
    if  GEMINI_INTEGRATION == selected_llm.integration:
        response_data = chat_gemini(conversation['messages'])
    elif NGROK_INTEGRATION == selected_llm.integration:
        # response_data = chat_ngrok(conversation['messages'])
        pass
    else:
        logger.warning(f'LLM {selected_llm.name} no tiene implementación de servicio, usando gemini como fallback')
        response_data = chat_gemini(conversation['messages'])
    
    if response_data.get('text'):
        conversation['messages'].append({
            'role': 'model',
            'content': response_data['text']
        })
    
    save_message(conversation)
    
    response_data['conversation_id'] = conversation_id
    
    return response_data

def get_conversation_history_by_id(conversation_id: str) -> Dict[str, Any]:
    return get_conversation_history(conversation_id)