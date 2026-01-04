from flask import Blueprint, request, jsonify
from app.services.gemini_service import test_gemini
from app.services.chat_orchestrator import ChatOrchestrator

llm_bp = Blueprint('llm', __name__)

orchestrator = ChatOrchestrator()

@llm_bp.route('/chat-test', methods=['GET'])
def test():
    response = test_gemini()
    return jsonify({
        'status': 'success',
        'message': response
    }), 200

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