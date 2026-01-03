import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    if not email:
        return False, 'El email es requerido'
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, 'Formato de email inválido'
    
    return True, ''


def validate_password(password: str) -> Tuple[bool, str]:
    if not password:
        return False, 'La contraseña es requerida'
    
    if len(password) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres'
    
    if not re.search(r'[A-Z]', password):
        return False, 'La contraseña debe contener al menos una letra mayúscula'
    
    if not re.search(r'[a-z]', password):
        return False, 'La contraseña debe contener al menos una letra minúscula'
    
    if not re.search(r'\d', password):
        return False, 'La contraseña debe contener al menos un número'
    
    return True, ''
