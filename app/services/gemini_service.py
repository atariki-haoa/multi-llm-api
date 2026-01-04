from google import genai
from app.utils.logger import get_logger
from app.utils.model_selector import gemini_model_selector
from typing import Dict, Any, List

logger = get_logger(__name__)

def test_gemini():
    logger.info('Iniciando prueba de Gemini API')
    
    try:
        client = genai.Client()
        logger.debug('Cliente de Gemini inicializado')
        
        response = client.models.generate_content(
            model=gemini_model_selector(), contents="Explain how AI works in a few words"
        )
        
        logger.info('Respuesta recibida de Gemini API exitosamente')
        return response.text
    except Exception as e:
        logger.error(f'Error al llamar a Gemini API: {str(e)}', exc_info=True)
        raise

def map_messages(messages: list) -> list:
    mapped_messages = []
    for message in messages:
        role = message['role']
        if role == 'assistant':
            role = 'model'
        mapped_messages.append({
            'role': role,
            'content': message['content']
        })
    return mapped_messages
def map_interaction_response(interaction: Any) -> Dict[str, Any]:
    mapped_response = {
        'text': None,
        'content': None,
        'outputs': [],
        'model': None,
        'usage': {},
        'finish_reason': None,
        'safety_ratings': [],
        'citations': [],
        'grounding_metadata': None
    }
    
    try:
        if hasattr(interaction, 'outputs') and interaction.outputs:
            for output in interaction.outputs:
                output_data = {
                    'type': getattr(output, 'type', None),
                    'text': getattr(output, 'text', None),
                    'content': getattr(output, 'content', None)
                }
                
                if hasattr(output, 'safety_ratings'):
                    output_data['safety_ratings'] = [
                        {
                            'category': getattr(rating, 'category', None),
                            'probability': getattr(rating, 'probability', None),
                            'blocked': getattr(rating, 'blocked', None)
                        } for rating in output.safety_ratings
                    ]
                
                if hasattr(output, 'citations'):
                    output_data['citations'] = [
                        {
                            'start_index': getattr(citation, 'start_index', None),
                            'end_index': getattr(citation, 'end_index', None),
                            'uri': getattr(citation, 'uri', None),
                            'title': getattr(citation, 'title', None),
                            'license': getattr(citation, 'license', None)
                        } for citation in output.citations
                    ]
                
                mapped_response['outputs'].append(output_data)
                
                if output_data['text']:
                    if mapped_response['text']:
                        mapped_response['text'] += '\n' + output_data['text']
                    else:
                        mapped_response['text'] = output_data['text']
        
        if hasattr(interaction, 'response'):
            response_obj = interaction.response
            if hasattr(response_obj, 'text'):
                mapped_response['text'] = response_obj.text
            if hasattr(response_obj, 'content'):
                mapped_response['content'] = response_obj.content
        
        if hasattr(interaction, 'text'):
            mapped_response['text'] = interaction.text
        
        if hasattr(interaction, 'model'):
            mapped_response['model'] = str(interaction.model)
        
        if hasattr(interaction, 'usage'):
            usage = interaction.usage
            mapped_response['usage'] = {
                'prompt_tokens': getattr(usage, 'prompt_token_count', None) or getattr(usage, 'prompt_tokens', None),
                'completion_tokens': getattr(usage, 'completion_token_count', None) or getattr(usage, 'completion_tokens', None),
                'total_tokens': getattr(usage, 'total_token_count', None) or getattr(usage, 'total_tokens', None)
            }
        
        if hasattr(interaction, 'finish_reason'):
            mapped_response['finish_reason'] = str(interaction.finish_reason)
        
        if hasattr(interaction, 'safety_ratings'):
            mapped_response['safety_ratings'] = [
                {
                    'category': getattr(rating, 'category', None),
                    'probability': getattr(rating, 'probability', None),
                    'blocked': getattr(rating, 'blocked', None)
                } for rating in interaction.safety_ratings
            ]
        
        if hasattr(interaction, 'citations'):
            mapped_response['citations'] = [
                {
                    'start_index': getattr(citation, 'start_index', None),
                    'end_index': getattr(citation, 'end_index', None),
                    'uri': getattr(citation, 'uri', None),
                    'title': getattr(citation, 'title', None),
                    'license': getattr(citation, 'license', None)
                } for citation in interaction.citations
            ]
        
        if hasattr(interaction, 'grounding_metadata'):
            grounding = interaction.grounding_metadata
            mapped_response['grounding_metadata'] = {
                'web_search_queries': getattr(grounding, 'web_search_queries', []),
                'grounding_chunks': getattr(grounding, 'grounding_chunks', [])
            }
        
    except Exception as e:
        logger.warning(f'Error al mapear respuesta: {str(e)}')
    
    return mapped_response

def chat_gemini(messages: list) -> Dict[str, Any]:
    logger.info('Iniciando chat con Gemini API')
    
    try:
        client = genai.Client()
        logger.debug('Cliente de Gemini inicializado')
        mapped_messages = map_messages(messages)
        interaction = client.interactions.create(
            model=gemini_model_selector(),
            input=mapped_messages
        )
        
        logger.info('Respuesta recibida de Gemini API exitosamente')
        mapped_response = map_interaction_response(interaction)
        
        return mapped_response
    except Exception as e:
        logger.error(f'Error al llamar a Gemini API: {str(e)}', exc_info=True)
        raise