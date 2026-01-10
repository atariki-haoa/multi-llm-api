from flask import Blueprint, request, jsonify
from app.services.chat_orchestrator import ChatOrchestrator
from app.services.llm.gemini_llm_service import GeminiLLMService

llm_bp = Blueprint('llm', __name__)

orchestrator = ChatOrchestrator()

@llm_bp.route('/chat-test', methods=['GET'])
def test():
    try:
        gemini_service = GeminiLLMService()
        response = gemini_service.chat([
            {'role': 'user', 'content': 'Hola, responde solo con "Test exitoso"'}
        ])
        return jsonify({
            'status': 'success',
            'message': response
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@llm_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    conversation_id = data.get('conversation_id')
    
    if not message:
        return jsonify({
            'status': 'error',
            'message': 'El campo "message" es requerido'
        }), 400
    
    try:
        response_data = orchestrator.chat(message, conversation_id)
        return jsonify({
            'status': 'success',
            'data': response_data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@llm_bp.route('/get-conversation-history', methods=['GET'])
def get_conversation_history():
    conversation_id = request.args.get('conversation_id')
    if not conversation_id:
        return jsonify({
            'status': 'error',
            'message': 'El campo "conversation_id" es requerido'
        }), 400
    try:
        return jsonify({
            'status': 'success',
            'data': orchestrator.get_history(conversation_id)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500