from typing import Dict, Optional
from app.services.llm.base_llm_service import BaseLLMService
from app.services.llm.gemini_llm_service import GeminiLLMService
from app.services.llm.ngrok_llm_service import NgrokLLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMServiceFactory:
    _services: Dict[str, BaseLLMService] = {}
    _initialized = False
    
    @classmethod
    def _initialize(cls):
        if not cls._initialized:
            cls.register_service(GeminiLLMService())
            cls.register_service(NgrokLLMService())
            cls._initialized = True
            logger.info('LLMServiceFactory inicializado con servicios disponibles')
    
    @classmethod
    def register_service(cls, service: BaseLLMService):
        integration_name = service.get_integration_name()
        cls._services[integration_name] = service
        logger.debug(f'Servicio registrado: {integration_name}')
    
    @classmethod
    def get_service(cls, integration: str) -> Optional[BaseLLMService]:
        cls._initialize()
        
        service = cls._services.get(integration)
        if service:
            logger.debug(f'Servicio encontrado para integración: {integration}')
            return service
        
        logger.warning(f'No se encontró servicio para integración: {integration}')
        return None
    
    @classmethod
    def get_all_services(cls) -> Dict[str, BaseLLMService]:
        cls._initialize()
        return cls._services.copy()
