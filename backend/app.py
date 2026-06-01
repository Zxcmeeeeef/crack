from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crack.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this'
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import routes
from routes import auth, messages, users, channels

app.register_blueprint(auth.auth_bp)
app.register_blueprint(messages.messages_bp)
app.register_blueprint(users.users_bp)
app.register_blueprint(channels.channels_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'CRACK Social Network'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
