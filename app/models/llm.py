from datetime import datetime, timezone
from app.models.base import db


class LLM(db.Model):
    __tablename__ = 'llm'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    integration = db.Column(db.String(100), nullable=False, default='gemini')
    priority = db.Column(db.Integer, nullable=False, default=0)
    rpm = db.Column(db.Integer, nullable=False, default=0)
    tpm = db.Column(db.Integer, nullable=False, default=0)
    rpd = db.Column(db.Integer, nullable=False, default=0)
    api_key = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    usages = db.relationship('Usage', backref='llm', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LLM {self.name}>'
