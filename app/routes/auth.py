from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Username, email y password son requeridos'}), 400
    
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        user = AuthService.create_user(username, email, password)
        tokens = AuthService.generate_tokens(user)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict(),
            **tokens
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al registrar usuario'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username y password son requeridos'}), 400
    
    user = AuthService.authenticate_user(username, password)
    
    if not user:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    tokens = AuthService.generate_tokens(user)
    
    return jsonify({
        'message': 'Login exitoso',
        'user': user.to_dict(),
        **tokens
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'error': 'Refresh token requerido'}), 400
    
    result = AuthService.refresh_access_token(refresh_token)
    
    if not result:
        return jsonify({'error': 'Refresh token inválido o expirado'}), 401
    
    return jsonify(result), 200
