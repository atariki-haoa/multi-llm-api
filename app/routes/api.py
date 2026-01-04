from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import auth_required, get_current_user
from app.utils.logger import get_logger

api_bp = Blueprint('api', __name__)
logger = get_logger(__name__)

@api_bp.route('/health', methods=['GET'])
def health():
    logger.debug('Health check solicitado')
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando correctamente'
    }), 200
