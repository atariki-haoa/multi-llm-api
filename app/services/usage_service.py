from flask import current_app
from app.repositories.usage import UsageRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UsageService:
    def __init__(self, repository: UsageRepository = None):
        self.repository = repository or UsageRepository
    
    def increment(self, llm_id: int) -> bool:
        with current_app.app_context():
            usage = self.repository.find_by_llm_id(llm_id)
            if usage:
                self.repository.increment_rpd(llm_id)
                logger.debug(f'Uso incrementado para LLM {llm_id}')
                return True
            else:
                self.repository.create(llm_id, rpd_count=1)
                logger.debug(f'Uso creado e incrementado para LLM {llm_id}')
                return True
    
    def reset(self, llm_id: int) -> bool:
        with current_app.app_context():
            return self.repository.reset_rpd(llm_id)
    
    def get_usage(self, llm_id: int) -> int:
        with current_app.app_context():
            usage = self.repository.find_by_llm_id(llm_id)
            return usage.rpd_count if usage else 0
