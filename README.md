# Multi-LLM API

API REST construida con Flask que proporciona autenticación JWT y capacidad para conectarse a APIs externas.

## Características

- ✅ Autenticación JWT (Access y Refresh tokens)
- ✅ Estructura de proyecto modular y escalable
- ✅ Servicio para conexión a APIs externas con retry automático
- ✅ Validación de datos de entrada
- ✅ Configuración mediante variables de entorno
- ✅ CORS habilitado

## Estructura del Proyecto

```
multi-llm-api/
├── app/
│   ├── __init__.py          # Factory de la aplicación
│   ├── config.py            # Configuraciones
│   ├── models/              # Modelos de base de datos
│   │   └── user.py
│   ├── routes/              # Blueprints de rutas
│   │   ├── auth.py          # Rutas de autenticación
│   │   └── api.py           # Rutas de API
│   ├── services/            # Lógica de negocio
│   │   ├── auth_service.py
│   │   └── external_api_service.py
│   ├── middleware/          # Middleware y decoradores
│   │   └── auth_middleware.py
│   └── utils/               # Utilidades
│       └── validators.py
├── tests/                   # Tests unitarios
├── run.py                   # Punto de entrada
├── requirements.txt         # Dependencias
└── .env.example            # Ejemplo de variables de entorno
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores
```

5. Inicializar la base de datos:
```bash
python run.py
```

## Uso

### Iniciar el servidor

```bash
python run.py
```

El servidor estará disponible en `http://localhost:5000`

### Endpoints de Autenticación

#### Registrar usuario
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "Password123"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "Password123"
}
```

#### Refrescar token
```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "tu_refresh_token"
}
```

### Endpoints de API (Requieren autenticación)

#### Health Check
```bash
GET /api/health
```

#### Obtener perfil
```bash
GET /api/profile
Authorization: Bearer {access_token}
```

#### Llamada GET a API externa
```bash
POST /api/external/get
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://api.externa.com/endpoint",
  "headers": {
    "X-API-Key": "tu-api-key"
  },
  "params": {
    "param1": "value1"
  }
}
```

#### Llamada POST a API externa
```bash
POST /api/external/post
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://api.externa.com/endpoint",
  "headers": {
    "Content-Type": "application/json"
  },
  "payload": {
    "key": "value"
  },
  "use_json": true
}
```

#### Llamada PUT a API externa
```bash
POST /api/external/put
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://api.externa.com/endpoint",
  "headers": {
    "Content-Type": "application/json"
  },
  "payload": {
    "key": "value"
  },
  "use_json": true
}
```

#### Llamada DELETE a API externa
```bash
POST /api/external/delete
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://api.externa.com/endpoint",
  "headers": {
    "X-API-Key": "tu-api-key"
  }
}
```

## Variables de Entorno

- `SECRET_KEY`: Clave secreta de Flask
- `JWT_SECRET_KEY`: Clave secreta para JWT
- `DATABASE_URL`: URL de conexión a la base de datos
- `EXTERNAL_API_TIMEOUT`: Timeout para llamadas externas (segundos)
- `EXTERNAL_API_MAX_RETRIES`: Número máximo de reintentos
- `RATE_LIMIT_ENABLED`: Habilitar rate limiting (true/false)
- `RATE_LIMIT_PER_MINUTE`: Límite de requests por minuto

## Seguridad

- Las contraseñas se almacenan con hash usando Werkzeug
- Los tokens JWT tienen expiración configurable
- Validación de email y contraseña fuerte
- Middleware de autenticación para proteger endpoints

## Desarrollo

Para ejecutar en modo desarrollo:
```bash
export FLASK_ENV=development
python run.py
```

## Licencia

Ver archivo LICENSE
