from functools import wraps
from flask import request, jsonify, g
from app.services.auth_service import AuthService
from app.models.user import User


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token de autenticación requerido'}), 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Formato de token inválido'}), 401
        
        payload = AuthService.verify_token(token, token_type='access')
        
        if not payload:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        user = User.query.get(payload['user_id'])
        
        if not user or not user.is_active:
            return jsonify({'error': 'Usuario no encontrado o inactivo'}), 401
        
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user() -> User:
    return g.current_user
