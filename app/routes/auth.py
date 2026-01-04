from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_password
from app.utils.logger import get_logger

auth_bp = Blueprint('auth', __name__)
logger = get_logger(__name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    logger.info('Solicitud de registro recibida')
    data = request.get_json()
    
    if not data:
        logger.warning('Intento de registro sin datos')
        return jsonify({'error': 'Datos requeridos'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        logger.warning('Intento de registro con campos faltantes')
        return jsonify({'error': 'Username, email y password son requeridos'}), 400
    
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        logger.warning(f'Intento de registro con email inválido: {email}')
        return jsonify({'error': error_msg}), 400
    
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        logger.warning('Intento de registro con contraseña inválida')
        return jsonify({'error': error_msg}), 400
    
    try:
        user = AuthService.create_user(username, email, password)
        tokens = AuthService.generate_tokens(user)
        
        logger.info(f'Registro exitoso para usuario: {username}')
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict(),
            **tokens
        }), 201
    except ValueError as e:
        logger.warning(f'Error de validación en registro: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error inesperado en registro: {str(e)}', exc_info=True)
        return jsonify({'error': 'Error al registrar usuario'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    logger.info('Solicitud de login recibida')
    data = request.get_json()
    
    if not data:
        logger.warning('Intento de login sin datos')
        return jsonify({'error': 'Datos requeridos'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logger.warning('Intento de login con campos faltantes')
        return jsonify({'error': 'Username y password son requeridos'}), 400
    
    user = AuthService.authenticate_user(username, password)
    
    if not user:
        logger.warning(f'Intento de login fallido para usuario: {username}')
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    tokens = AuthService.generate_tokens(user)
    
    logger.info(f'Login exitoso para usuario: {username}')
    
    return jsonify({
        'message': 'Login exitoso',
        'user': user.to_dict(),
        **tokens
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    logger.debug('Solicitud de refresh token recibida')
    data = request.get_json()
    
    if not data:
        logger.warning('Intento de refresh sin datos')
        return jsonify({'error': 'Datos requeridos'}), 400
    
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        logger.warning('Intento de refresh sin token')
        return jsonify({'error': 'Refresh token requerido'}), 400
    
    result = AuthService.refresh_access_token(refresh_token)
    
    if not result:
        logger.warning('Intento de refresh con token inválido o expirado')
        return jsonify({'error': 'Refresh token inválido o expirado'}), 401
    
    logger.info('Refresh token exitoso')
    
    return jsonify(result), 200
