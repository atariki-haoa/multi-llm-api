import os
from app import create_app
from app import db
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = create_app(Config)
PORT = os.environ.get('PORT', 9000)

if __name__ == '__main__':
    logger.info(f'Iniciando servidor Flask en puerto {PORT}')
    
    with app.app_context():
        db.create_all()
        logger.info('Base de datos inicializada')
    
    logger.info(f'Servidor corriendo en http://0.0.0.0:{PORT}')
    app.run(debug=True, host='0.0.0.0', port=PORT)
