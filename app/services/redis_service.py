import json
import redis
import os
import uuid
from typing import List, Dict, Optional
from flask import current_app
from app.utils.logger import get_logger

logger = get_logger(__name__)

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=os.environ.get('REDIS_HOST', 'localhost'),
                port=int(os.environ.get('REDIS_PORT', 6379)),
                db=int(os.environ.get('REDIS_DB', 0)),
                password=os.environ.get('REDIS_PASSWORD'),
                decode_responses=True,
                socket_connect_timeout=5
            )
            _redis_client.ping()
            logger.info('Cliente Redis conectado exitosamente')
        except Exception as e:
            logger.error(f'Error al conectar con Redis: {str(e)}', exc_info=True)
            raise
    return _redis_client

def get_conversation_key(conversation_id: str) -> str:
    return f"conversation:{conversation_id}"

def create_conversation(model: str, message: str) -> dict:
    try:
        client = get_redis_client()
        conversation_id = str(uuid.uuid4())
        messages = [{'role': 'user', 'content': message}]
        key = get_conversation_key(conversation_id)
        
        conversation_data = {
            'model': model,
            'messages': messages,
            'conversation_id': conversation_id
        }
        
        ttl = int(os.environ.get('REDIS_CONVERSATION_TTL', 86400))
        client.setex(key, ttl, json.dumps(conversation_data))
        logger.debug(f'Conversación creada: {conversation_id}')
        return {'conversation_id': conversation_id, 'model': model, 'messages': messages}
    except Exception as e:
        logger.error(f'Error al crear conversación: {str(e)}', exc_info=True)
        return None

def save_message(conversation: dict) -> bool:
    try:
        client = get_redis_client()
        conversation_id = conversation.get('conversation_id')
        if not conversation_id:
            logger.error('conversation_id no encontrado en el objeto conversación')
            return False
        
        key = get_conversation_key(conversation_id)
        
        messages = conversation.get('messages', [])
        model = conversation.get('model', '')
        
        conversation_data = {
            'model': model,
            'messages': messages,
            'conversation_id': conversation_id
        }
        
        ttl = int(os.environ.get('REDIS_CONVERSATION_TTL', 86400))
        client.setex(key, ttl, json.dumps(conversation_data))
        
        logger.debug(f'Conversación guardada: {conversation_id} con {len(messages)} mensajes')
        return True
    except Exception as e:
        logger.error(f'Error al guardar mensaje: {str(e)}', exc_info=True)
        return False

def get_conversation_history(conversation_id: str) -> dict:
    try:
        client = get_redis_client()
        key = get_conversation_key(conversation_id)
        
        conversation_data = client.get(key)
        if conversation_data:
            data = json.loads(conversation_data)
            if 'conversation_id' not in data:
                data['conversation_id'] = conversation_id
            logger.debug(f'Historial recuperado para conversación {conversation_id}: {len(data.get("messages", []))} mensajes')
            return data
        else:
            logger.debug(f'No se encontró historial para conversación {conversation_id}')
            return {'model': '', 'messages': [], 'conversation_id': conversation_id}
    except Exception as e:
        logger.error(f'Error al recuperar historial: {str(e)}', exc_info=True)
        return {'model': '', 'messages': [], 'conversation_id': conversation_id}

def delete_conversation(conversation_id: str) -> bool:
    try:
        client = get_redis_client()
        key = get_conversation_key(conversation_id)
        deleted = client.delete(key)
        logger.info(f'Conversación {conversation_id} eliminada: {deleted > 0}')
        return deleted > 0
    except Exception as e:
        logger.error(f'Error al eliminar conversación: {str(e)}', exc_info=True)
        return False

def clear_all_conversations() -> bool:
    try:
        client = get_redis_client()
        keys = client.keys("conversation:*")
        if keys:
            deleted = client.delete(*keys)
            logger.info(f'{deleted} conversaciones eliminadas')
            return True
        return True
    except Exception as e:
        logger.error(f'Error al limpiar conversaciones: {str(e)}', exc_info=True)
        return False