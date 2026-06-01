from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

from app import db
from models import User

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@users_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify({'error': 'Query too short'}), 400
    
    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) |
        (User.first_name.ilike(f'%{query}%'))
    ).limit(10).all()
    
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.bio = data.get('bio', user.bio)
    user.avatar_url = data.get('avatar_url', user.avatar_url)
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200
