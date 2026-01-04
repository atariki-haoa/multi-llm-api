from functools import wraps
from flask import request, jsonify, g
from app.services.auth_service import AuthService
from app.models.user import User
from app.utils.logger import get_logger

logger = get_logger(__name__)


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning(f'Intento de acceso sin token a {request.path}')
            return jsonify({'error': 'Token de autenticación requerido'}), 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            logger.warning(f'Formato de token inválido en {request.path}')
            return jsonify({'error': 'Formato de token inválido'}), 401
        
        payload = AuthService.verify_token(token, token_type='access')
        
        if not payload:
            logger.warning(f'Token inválido o expirado en {request.path}')
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        user = User.query.get(payload['user_id'])
        
        if not user or not user.is_active:
            logger.warning(f'Usuario no encontrado o inactivo: {payload.get("user_id")}')
            return jsonify({'error': 'Usuario no encontrado o inactivo'}), 401
        
        g.current_user = user
        logger.debug(f'Usuario autenticado accediendo a {request.path}: {user.username}')
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user() -> User:
    return g.current_user
