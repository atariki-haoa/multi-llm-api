from app import create_app
from app.config import Config
from app.models.base import db
from app.models.llm import LLM
from app.models.usage import Usage
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv
load_dotenv()

logger = get_logger(__name__)


def seed_database():
    app = create_app(Config)
    
    with app.app_context():
        db.create_all()
        
        logger.info('Iniciando seeder de base de datos...')
        
        llm_data = [
            {
                'name': 'gemini-2.5-flash',
                'integration': 'gemini',
                'priority': 1,
                'rpm': 5,
                'tpm': 250000,
                'rpd': 20,
                'api_key': os.getenv('GEMINI_API_KEY')
            },
            {
                'name': 'gemma-3-27b',
                'integration': 'gemini',
                'priority': 3,
                'rpm': 30,
                'tpm': 15000,
                'rpd': 14400,
                'api_key': os.getenv('GEMINI_API_KEY')
            },
            {
                'name': 'ngrok',
                'integration': 'ngrok',
                'priority': 2,
                'rpm': 120,
                'tpm': 0,
                'rpd': 650,
                'api_key': os.getenv('NGROK_API_KEY')
            },
        ]
        
        existing_llms = LLM.query.all()
        if existing_llms:
            logger.warning(f'Ya existen {len(existing_llms)} registros en la tabla LLM. Eliminando...')
            for llm in existing_llms:
                db.session.delete(llm)
            db.session.commit()
        
        existing_usages = Usage.query.all()
        if existing_usages:
            logger.warning(f'Ya existen {len(existing_usages)} registros en la tabla Usage. Eliminando...')
            for usage in existing_usages:
                db.session.delete(usage)
            db.session.commit()
        
        logger.info('Creando registros LLM...')
        created_llms = []
        for llm_info in llm_data:
            llm = LLM(**llm_info)
            db.session.add(llm)
            created_llms.append(llm)
        
        db.session.commit()
        logger.info(f'Creados {len(created_llms)} registros LLM')
        
        logger.info('Creando registros Usage...')
        for llm in created_llms:
            usage = Usage(rpd_count=0, llm_id=llm.id)
            db.session.add(usage)
        
        db.session.commit()
        logger.info(f'Creados {len(created_llms)} registros Usage')
        
        logger.info('Seeder completado exitosamente')
        
        logger.info('Resumen de datos creados:')
        all_llms = LLM.query.all()
        for llm in all_llms:
            logger.info(f'  - LLM: {llm.name} (ID: {llm.id}, Priority: {llm.priority})')
            usage = Usage.query.filter_by(llm_id=llm.id).first()
            if usage:
                logger.info(f'    Usage: RPD Count = {usage.rpd_count}')


if __name__ == '__main__':
    seed_database()
