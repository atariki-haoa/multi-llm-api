from typing import Optional
from app.models.usage import Usage
from app.models.base import db
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UsageRepository:
    @staticmethod
    def find_by_llm_id(llm_id: int) -> Optional[Usage]:
        return Usage.query.filter_by(llm_id=llm_id).first()
    
    @staticmethod
    def create(llm_id: int, rpd_count: int = 1) -> Usage:
        usage = Usage(llm_id=llm_id, rpd_count=rpd_count)
        db.session.add(usage)
        db.session.commit()
        logger.debug(f'Usage creado para LLM {llm_id}')
        return usage
    
    @staticmethod
    def increment_rpd(llm_id: int) -> bool:
        usage = UsageRepository.find_by_llm_id(llm_id)
        if usage:
            usage.rpd_count += 1
            db.session.commit()
            logger.debug(f'RPD incrementado para LLM {llm_id}: {usage.rpd_count}')
            return True
        return False
    
    @staticmethod
    def reset_rpd(llm_id: int) -> bool:
        usage = UsageRepository.find_by_llm_id(llm_id)
        if usage:
            usage.rpd_count = 0
            db.session.commit()
            logger.info(f'RPD reseteado para LLM {llm_id}')
            return True
        return False
