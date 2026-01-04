from typing import Optional, List, Tuple
from app.models.llm import LLM
from app.models.usage import Usage
from app.models.base import db

class LLMRepository:
    @staticmethod
    def find_available_llms() -> List[Tuple[LLM, Usage]]:
        return db.session.query(LLM, Usage).join(
            Usage, LLM.id == Usage.llm_id
        ).filter(
            Usage.rpd_count < LLM.rpd
        ).order_by(LLM.priority.asc()).all()
    
    @staticmethod
    def find_all_llms_ordered() -> List[Tuple[LLM, Usage]]:
        return db.session.query(LLM, Usage).join(
            Usage, LLM.id == Usage.llm_id
        ).order_by(LLM.priority.asc()).all()
    
    @staticmethod
    def find_by_id(llm_id: int) -> Optional[LLM]:
        return LLM.query.get(llm_id)