from app import create_app
from app.config import Config
from app.models.base import db
from app.utils.logger import get_logger
from sqlalchemy import text

logger = get_logger(__name__)


def migrate_add_integration():
    app = create_app(Config)
    
    with app.app_context():
        try:
            logger.info('Verificando si la columna integration existe...')
            
            result = db.session.execute(text("PRAGMA table_info(llm)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'integration' in columns:
                logger.info('La columna integration ya existe, no es necesario migrar')
                return
            
            logger.info('Agregando columna integration a la tabla llm...')
            db.session.execute(text('''
                ALTER TABLE llm 
                ADD COLUMN integration VARCHAR(100) DEFAULT 'gemini'
            '''))
            db.session.commit()
            
            logger.info('Columna integration agregada exitosamente')
            
            result = db.session.execute(text('SELECT id, name FROM llm'))
            existing_llms = result.fetchall()
            
            if existing_llms:
                logger.info(f'Actualizando {len(existing_llms)} registros existentes...')
                for llm_id, name in existing_llms:
                    integration = 'ngrok' if 'ngrok' in name.lower() else 'gemini'
                    db.session.execute(
                        text('UPDATE llm SET integration = :integration WHERE id = :id'),
                        {'integration': integration, 'id': llm_id}
                    )
                db.session.commit()
                logger.info('Registros actualizados exitosamente')
            else:
                logger.info('No hay registros que actualizar')
            
        except Exception as e:
            db.session.rollback()
            if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
                logger.info('La columna integration ya existe, no es necesario migrar')
            else:
                logger.error(f'Error durante la migración: {str(e)}')
                raise


if __name__ == '__main__':
    migrate_add_integration()
