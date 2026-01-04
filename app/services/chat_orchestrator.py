from typing import Dict, Any, Optional
from app.services.llm_selector_service import LLMSelectorService
from app.services.conversation_service import ConversationService
from app.services.usage_service import UsageService
from app.factories.llm_service_factory import LLMServiceFactory
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatOrchestrator:
    def __init__(
        self,
        selector: LLMSelectorService = None,
        conversation_service: ConversationService = None,
        usage_service: UsageService = None
    ):
        self.selector = selector or LLMSelectorService()
        self.conversation_service = conversation_service or ConversationService()
        self.usage_service = usage_service or UsageService()
    
    def chat(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f'Iniciando chat - conversation_id: {conversation_id}')
        
        llm = self.selector.select_llm()
        
        conversation = self.conversation_service.get_or_create(
            conversation_id, llm.name, message
        )
        
        llm_service = LLMServiceFactory.get_service(llm.integration)
        if not llm_service:
            logger.error(f'Servicio no disponible para integración: {llm.integration}')
            raise ValueError(f'Servicio no disponible para {llm.integration}')
        
        response = llm_service.chat(conversation['messages'])
        
        self.conversation_service.save_response(
            conversation, response.get('text', '')
        )
        self.usage_service.increment(llm.id)
        
        response['conversation_id'] = conversation['conversation_id']
        
        logger.info(f'Chat completado - conversation_id: {conversation["conversation_id"]}')
        return response
    
    def get_history(self, conversation_id: str) -> Dict[str, Any]:
        return self.conversation_service.get_history(conversation_id)
