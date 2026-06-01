from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('Message', backref='sender', lazy=True)
    channels = db.relationship('Channel', secondary='channel_members', backref='members')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'is_online': self.is_online,
            'created_at': self.created_at.isoformat()
        }

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    avatar_url = db.Column(db.String(255))
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_channels')
    messages = db.relationship('Message', backref='channel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator_id': self.creator_id,
            'avatar_url': self.avatar_url,
            'is_private': self.is_private,
            'members_count': len(self.members),
            'created_at': self.created_at.isoformat()
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'sender': self.sender.to_dict(),
            'channel_id': self.channel_id,
            'is_edited': self.is_edited,
            'edited_at': self.edited_at.isoformat() if self.edited_at else None,
            'created_at': self.created_at.isoformat()
        }

# Association table for channel members
channel_members = db.Table('channel_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)
