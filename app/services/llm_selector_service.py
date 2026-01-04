from flask import current_app
from app.repositories.llm import LLMRepository
from app.models.llm import LLM
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMSelectorService:
    def __init__(self, repository: LLMRepository = None):
        self.repository = repository or LLMRepository
    
    def select_llm(self) -> LLM:
        with current_app.app_context():
            llms_with_usage = self.repository.find_available_llms()
            
            if not llms_with_usage:
                logger.warning('No hay LLMs disponibles (todos han excedido su límite rpd), seleccionando el de menor prioridad')
                llms_with_usage = self.repository.find_all_llms_ordered()
            
            if not llms_with_usage:
                logger.error('No hay LLMs configurados en la base de datos')
                raise ValueError('No hay LLMs disponibles en la base de datos')
            
            selected_llm, usage = llms_with_usage[0]
            logger.info(f'LLM seleccionado: {selected_llm.name} (priority: {selected_llm.priority}, rpd_count: {usage.rpd_count}/{selected_llm.rpd})')
            
            return selected_llm
