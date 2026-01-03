from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from flask import current_app
from app.models.user import User
from app import db


class AuthService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        if User.query.filter_by(username=username).first():
            raise ValueError('El nombre de usuario ya existe')
        
        if User.query.filter_by(email=email).first():
            raise ValueError('El email ya está registrado')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.is_active:
            return None
        
        if not user.check_password(password):
            return None
        
        user.last_login = datetime.timezone.utc()
        db.session.commit()
        
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
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.timezone.utc() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.timezone.utc(),
            'type': 'access'
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def _generate_refresh_token(user: User) -> str:
        payload = {
            'user_id': user.id,
            'exp': datetime.timezone.utc() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.timezone.utc(),
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
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
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
