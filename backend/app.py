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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'CRACK Social Network'}), 200

if __name__ == '__main__':
    with app.app_context():
        from models import User, Channel, Message
        db.create_all()
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.messages import messages_bp
    from routes.users import users_bp
    from routes.channels import channels_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(channels_bp)
    
    app.run(debug=True, host='0.0.0.0', port=5000)