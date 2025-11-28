from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ========== RESTAURANT MODEL ==========
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_menu=False):
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'rating': self.rating,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_menu:
            menu_items = MenuItem.query.filter_by(restaurant_id=self.id).all()
            result['menu'] = [item.to_dict() for item in menu_items]
            
        return result

# ========== MENU ITEM MODEL ==========
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    restaurant = db.relationship('Restaurant', backref=db.backref('menu_items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def create_tables():
    with app.app_context():
        db.create_all()
        print("Restaurant Service tables created")

# ========================
# CRUD ENDPOINTS (4 Methods)
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "restaurant-service",
        "timestamp": datetime.utcnow().isoformat()
    })

# GET - List all restaurants
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """GET - List all restaurants"""
    try:
        include_menu = request.args.get('include_menu', 'false').lower() == 'true'
        restaurants = Restaurant.query.all()
        
        return jsonify({
            "success": True,
            "data": [r.to_dict(include_menu=include_menu) for r in restaurants],
            "count": len(restaurants)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET - Get single restaurant by ID (includes menu)
@app.route('/api/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    """GET - Get single restaurant with menu"""
    try:
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"success": False, "error": "Restaurant not found"}), 404

        return jsonify({
            "success": True,
            "data": restaurant.to_dict(include_menu=True)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# POST - Create new restaurant (with optional menu items)
@app.route('/api/restaurants', methods=['POST'])
def create_restaurant():
    """POST - Create new restaurant (can include menu items)"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({"success": False, "error": "Name is required"}), 400
        
        new_restaurant = Restaurant(
            name=data.get('name'),
            description=data.get('description', ''),
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            rating=data.get('rating', 0.0),
            is_active=data.get('is_active', True)
        )
        db.session.add(new_restaurant)
        db.session.flush()  # Get the ID before committing
        
        # Add menu items if provided
        if data.get('menu'):
            for item_data in data.get('menu'):
                menu_item = MenuItem(
                    restaurant_id=new_restaurant.id,
                    name=item_data.get('name'),
                    description=item_data.get('description', ''),
                    price=float(item_data.get('price')),
                    category=item_data.get('category'),
                    image_url=item_data.get('image_url'),
                    is_available=item_data.get('is_available', True)
                )
                db.session.add(menu_item)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": new_restaurant.to_dict(include_menu=True),
            "message": "Restaurant created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# PUT - Update restaurant (can update menu items too)
@app.route('/api/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id):
    """PUT - Update restaurant and menu"""
    try:
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"success": False, "error": "Restaurant not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Update restaurant fields
        if 'name' in data:
            restaurant.name = data['name']
        if 'description' in data:
            restaurant.description = data['description']
        if 'address' in data:
            restaurant.address = data['address']
        if 'phone' in data:
            restaurant.phone = data['phone']
        if 'email' in data:
            restaurant.email = data['email']
        if 'rating' in data:
            restaurant.rating = float(data['rating'])
        if 'is_active' in data:
            restaurant.is_active = data['is_active']

        # Update menu if provided
        if 'menu' in data:
            # Simple approach: delete existing menu and recreate
            MenuItem.query.filter_by(restaurant_id=id).delete()
            
            for item_data in data.get('menu', []):
                if item_data.get('name') and item_data.get('price'):
                    menu_item = MenuItem(
                        restaurant_id=id,
                        name=item_data.get('name'),
                        description=item_data.get('description', ''),
                        price=float(item_data.get('price')),
                        category=item_data.get('category'),
                        image_url=item_data.get('image_url'),
                        is_available=item_data.get('is_available', True)
                    )
                    db.session.add(menu_item)

        restaurant.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "success": True,
            "data": restaurant.to_dict(include_menu=True),
            "message": "Restaurant updated successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE - Delete restaurant (and its menu items)
@app.route('/api/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    """DELETE - Delete restaurant permanently"""
    try:
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"success": False, "error": "Restaurant not found"}), 404
        
        # Delete menu items first
        MenuItem.query.filter_by(restaurant_id=id).delete()
        
        # Delete restaurant
        db.session.delete(restaurant)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Restaurant deleted successfully"
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
    PORT = 5002  # rizki's Restaurant Service
    print(f"🍽️ Restaurant Service starting on port {PORT}")
    print(f"🩺 Health Check: http://localhost:{PORT}/health")
    print(f"Available endpoints (4 HTTP methods):")
    print(f"   GET    /api/restaurants          - List all restaurants")
    print(f"   GET    /api/restaurants/<id>     - Get restaurant with menu")
    print(f"   POST   /api/restaurants          - Create restaurant (with menu)")
    print(f"   PUT    /api/restaurants/<id>     - Update restaurant (and menu)")
    print(f"   DELETE /api/restaurants/<id>     - Delete restaurant")
    app.run(host='127.0.0.1', port=PORT, debug=True)