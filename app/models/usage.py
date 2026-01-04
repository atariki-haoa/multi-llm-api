from datetime import datetime, timezone
from app.models.base import db


class Usage(db.Model):
    __tablename__ = 'usage'
    
    id = db.Column(db.Integer, primary_key=True)
    rpd_count = db.Column(db.Integer, nullable=False, default=0)
    llm_id = db.Column(db.Integer, db.ForeignKey('llm.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<Usage LLM_ID={self.llm_id} RPD_COUNT={self.rpd_count}>'
