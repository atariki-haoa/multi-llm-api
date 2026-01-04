from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import register_routes
from app.models.base import db
from app.models import User, LLM, Usage
from app.utils.logger import setup_logger

logger = setup_logger('app')

__all__ = ['create_app', 'db', 'logger']

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logger.info('Inicializando aplicación Flask')
    
    db.init_app(app)
    CORS(app)
    
    register_routes(app)
    
    logger.info('Aplicación Flask inicializada correctamente')
    
    return app
