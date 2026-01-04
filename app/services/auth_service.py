from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from flask import current_app
from app.models.user import User
from app.models.base import db
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AuthService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        logger.info(f'Intentando crear usuario: {username}')
        
        if User.query.filter_by(username=username).first():
            logger.warning(f'Intento de registro con username duplicado: {username}')
            raise ValueError('El nombre de usuario ya existe')
        
        if User.query.filter_by(email=email).first():
            logger.warning(f'Intento de registro con email duplicado: {email}')
            raise ValueError('El email ya está registrado')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'Usuario creado exitosamente: {username} (ID: {user.id})')
        
        return user
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        logger.debug(f'Intentando autenticar usuario: {username}')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.is_active:
            logger.warning(f'Intento de autenticación fallido: usuario no encontrado o inactivo - {username}')
            return None
        
        if not user.check_password(password):
            logger.warning(f'Intento de autenticación fallido: contraseña incorrecta - {username}')
            return None
        
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        
        logger.info(f'Usuario autenticado exitosamente: {username} (ID: {user.id})')
        
        return user
    
    @staticmethod
    def generate_tokens(user: User) -> Dict[str, str]:
        access_token = AuthService._generate_access_token(user)
        refresh_token = AuthService._generate_refresh_token(user)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
    
    @staticmethod
    def _generate_access_token(user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': now,
            'type': 'access'
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def _generate_refresh_token(user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            'user_id': user.id,
            'exp': now + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': now,
            'type': 'refresh'
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_token(token: str, token_type: str = 'access') -> Optional[Dict]:
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            if payload.get('type') != token_type:
                logger.warning(f'Token con tipo incorrecto. Esperado: {token_type}')
                return None
            
            logger.debug(f'Token verificado exitosamente. Tipo: {token_type}, User ID: {payload.get("user_id")}')
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning('Intento de uso de token expirado')
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f'Token inválido: {str(e)}')
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
        payload = AuthService.verify_token(refresh_token, token_type='refresh')
        
        if not payload:
            return None
        
        user = User.query.get(payload['user_id'])
        
        if not user or not user.is_active:
            return None
        
        new_access_token = AuthService._generate_access_token(user)
        
        return {
            'access_token': new_access_token,
            'token_type': 'Bearer'
        }
