from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta
import os
import hashlib
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'food-delivery-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ========================
#  USER SERVICE MODELS
# ========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    user_type = db.Column(db.String(20), default='customer')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'user_type': self.user_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def create_tables():
    with app.app_context():
        db.create_all()
        print("User Service tables created")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ========================
# CRUD ENDPOINTS (4 Methods)
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "user-service",
        "timestamp": datetime.utcnow().isoformat()
    })

# GET - List all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    """GET - List all users"""
    try:
        users = User.query.all()
        return jsonify({
            "success": True,
            "data": [user.to_dict() for user in users],
            "count": len(users)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET - Get single user by ID
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    """GET - Get single user"""
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
            
        return jsonify({
            "success": True,
            "data": user.to_dict()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# POST - Create new user (supports action: login, register)
@app.route('/api/users', methods=['POST'])
def create_user():
    """POST - Create new user or login (use 'action' parameter)"""
    try:
        data = request.get_json()
        action = data.get('action', 'create')  # default: create
        
        # LOGIN ACTION
        if action == 'login':
            if not data.get('username') or not data.get('password'):
                return jsonify({"success": False, "error": "Username and password required"}), 400
            
            username = data.get('username')
            password = data.get('password')
            
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user or user.password_hash != hash_password(password):
                return jsonify({"success": False, "error": "Invalid credentials"}), 401
            
            if not user.is_active:
                return jsonify({"success": False, "error": "Account inactive"}), 400
            
            access_token = create_access_token(
                identity=user.username,
                additional_claims={
                    'id': user.id,
                    'email': user.email,
                    'role': user.user_type
                }
            )
            
            return jsonify({
                "success": True,
                "data": {
                    "user": user.to_dict(),
                    "token": access_token
                },
                "message": "Login successful"
            })
        
        # CREATE/REGISTER ACTION
        required_fields = ['username', 'email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        if not validate_email(data['email']):
            return jsonify({"success": False, "error": "Invalid email format"}), 400
        
        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return jsonify({"success": False, "error": "Username or email already exists"}), 409
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            full_name=data['full_name'],
            phone=data.get('phone'),
            address=data.get('address'),
            user_type=data.get('user_type', 'customer')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": new_user.to_dict(),
            "message": "User created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# PUT - Update user
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    """PUT - Update user"""
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'address' in data:
            user.address = data['address']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'password' in data:
            user.password_hash = hash_password(data['password'])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": user.to_dict(),
            "message": "User updated successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE - Delete user (hard delete)
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """DELETE - Delete user permanently"""
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "User deleted successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'success': False, 'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'success': False, 'error': 'Internal server error'}, 500

@app.errorhandler(400)
def bad_request(error):
    return {'success': False, 'error': 'Bad request'}, 400

if __name__ == '__main__':
    create_tables()
    PORT = 5001  # User Service
    print(f"User Service starting on port {PORT}")
    print(f"Health Check: http://localhost:{PORT}/health")
    print(f"Available endpoints (4 HTTP methods):")
    print(f"   GET    /api/users          - List all users")
    print(f"   GET    /api/users/<id>     - Get single user")
    print(f"   POST   /api/users          - Create user (or login with action=login)")
    print(f"   PUT    /api/users/<id>     - Update user")
    print(f"   DELETE /api/users/<id>     - Delete user")
    app.run(host='127.0.0.1', port=PORT, debug=True)