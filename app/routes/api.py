from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import auth_required, get_current_user
from app.services.external_api_service import ExternalAPIService

api_bp = Blueprint('api', __name__)
external_api = ExternalAPIService()


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando correctamente'
    }), 200
