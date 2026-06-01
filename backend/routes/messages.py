from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

from app import db
from models import Message, Channel, User

@messages_bp.route('/channel/<int:channel_id>', methods=['GET'])
@jwt_required()
def get_channel_messages(channel_id):
    channel = Channel.query.get(channel_id)
    
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    messages = Message.query.filter_by(channel_id=channel_id)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'messages': [msg.to_dict() for msg in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': page
    }), 200

@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('content') or not data.get('channel_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    channel = Channel.query.get(data['channel_id'])
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404
    
    message = Message(
        content=data['content'],
        sender_id=user_id,
        channel_id=data['channel_id']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required()
def edit_message(message_id):
    user_id = get_jwt_identity()
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    if message.sender_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    message.content = data.get('content', message.content)
    message.is_edited = True
    message.edited_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(message.to_dict()), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    user_id = get_jwt_identity()
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    if message.sender_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({'message': 'Message deleted'}), 200
