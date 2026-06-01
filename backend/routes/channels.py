from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

channels_bp = Blueprint('channels', __name__, url_prefix='/api/channels')

from app import db
from models import Channel, User, channel_members

@channels_bp.route('', methods=['GET'])
@jwt_required()
def get_channels():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    channels = user.channels
    return jsonify([channel.to_dict() for channel in channels]), 200

@channels_bp.route('', methods=['POST'])
@jwt_required()
def create_channel():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Missing channel name'}), 400
    
    channel = Channel(
        name=data['name'],
        description=data.get('description', ''),
        creator_id=user_id,
        is_private=data.get('is_private', False)
    )
    
    db.session.add(channel)
    db.session.flush()
    
    user = User.query.get(user_id)
    channel.members.append(user)
    
    db.session.commit()
    
    return jsonify(channel.to_dict()), 201

@channels_bp.route('/<int:channel_id>/join', methods=['POST'])
@jwt_required()
def join_channel(channel_id):
    user_id = get_jwt_identity()
    channel = Channel.query.get(channel_id)
    
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404
    
    user = User.query.get(user_id)
    
    if user in channel.members:
        return jsonify({'error': 'Already a member'}), 409
    
    channel.members.append(user)
    db.session.commit()
    
    return jsonify(channel.to_dict()), 200

@channels_bp.route('/<int:channel_id>/leave', methods=['POST'])
@jwt_required()
def leave_channel(channel_id):
    user_id = get_jwt_identity()
    channel = Channel.query.get(channel_id)
    
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404
    
    user = User.query.get(user_id)
    
    if user not in channel.members:
        return jsonify({'error': 'Not a member'}), 404
    
    channel.members.remove(user)
    db.session.commit()
    
    return jsonify({'message': 'Left channel'}), 200
