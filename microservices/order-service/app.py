from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ========================
#  ORDER SERVICE MODELS
# ========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, ready, delivered, cancelled
    total_price = db.Column(db.Float, default=0.0)
    delivery_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_items=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'order_number': self.order_number,
            'status': self.status,
            'total_price': self.total_price,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'is_paid': self.is_paid,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_items:
            items = OrderItem.query.filter_by(order_id=self.id).all()
            result['items'] = [item.to_dict() for item in items]
            
        return result

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, nullable=False)
    menu_item_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'menu_item_name': self.menu_item_name,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def create_tables():
    with app.app_context():
        db.create_all()
        print("Order Service tables created")

def generate_order_number():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{timestamp}-{random_str}"

# ========================
# CRUD ENDPOINTS (4 Methods)
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "order-service",
        "timestamp": datetime.utcnow().isoformat()
    })

# GET - List all orders
@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    """GET - List all orders"""
    try:
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        
        query = Order.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
            
        orders = query.all()
        
        return jsonify({
            "success": True,
            "data": [order.to_dict(include_items=True) for order in orders],
            "count": len(orders)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET - Get single order by ID
@app.route('/api/orders/<int:id>', methods=['GET'])
def get_order(id):
    """GET - Get single order with items"""
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({"success": False, "error": "Order not found"}), 404
            
        return jsonify({
            "success": True,
            "data": order.to_dict(include_items=True)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# POST - Create new order
@app.route('/api/orders', methods=['POST'])
def create_order():
    """POST - Create new order"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'restaurant_id', 'items']
        for field in required_fields:
            if not data or not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        if not isinstance(data.get('items'), list) or len(data.get('items')) == 0:
            return jsonify({"success": False, "error": "At least one item is required"}), 400
        
        # Create order
        new_order = Order(
            user_id=data['user_id'],
            restaurant_id=data['restaurant_id'],
            order_number=generate_order_number(),
            delivery_address=data.get('delivery_address'),
            notes=data.get('notes'),
            status=data.get('status', 'pending'),
            is_paid=data.get('is_paid', False)
        )
        
        db.session.add(new_order)
        db.session.flush()
        
        # Add order items
        total_price = 0
        for item_data in data['items']:
            if not item_data.get('menu_item_id') or not item_data.get('quantity') or not item_data.get('unit_price'):
                continue
                
            quantity = int(item_data['quantity'])
            unit_price = float(item_data['unit_price'])
            subtotal = quantity * unit_price
            total_price += subtotal
            
            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item_data['menu_item_id'],
                menu_item_name=item_data.get('menu_item_name', ''),
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal,
                notes=item_data.get('notes')
            )
            db.session.add(order_item)
        
        new_order.total_price = total_price
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": new_order.to_dict(include_items=True),
            "message": "Order created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# PUT - Update order (including status changes)
@app.route('/api/orders/<int:id>', methods=['PUT'])
def update_order(id):
    """PUT - Update order (status, address, items, etc.)"""
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({"success": False, "error": "Order not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update order fields
        if 'status' in data:
            order.status = data['status']
        if 'delivery_address' in data:
            order.delivery_address = data['delivery_address']
        if 'notes' in data:
            order.notes = data['notes']
        if 'is_paid' in data:
            order.is_paid = data['is_paid']
        
        # Update items if provided
        if 'items' in data:
            # Delete existing items
            OrderItem.query.filter_by(order_id=id).delete()
            
            # Add new items
            total_price = 0
            for item_data in data['items']:
                if item_data.get('menu_item_id') and item_data.get('quantity') and item_data.get('unit_price'):
                    quantity = int(item_data['quantity'])
                    unit_price = float(item_data['unit_price'])
                    subtotal = quantity * unit_price
                    total_price += subtotal
                    
                    order_item = OrderItem(
                        order_id=id,
                        menu_item_id=item_data['menu_item_id'],
                        menu_item_name=item_data.get('menu_item_name', ''),
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal,
                        notes=item_data.get('notes')
                    )
                    db.session.add(order_item)
            
            order.total_price = total_price
        
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": order.to_dict(include_items=True),
            "message": "Order updated successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE - Delete order
@app.route('/api/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    """DELETE - Delete order permanently"""
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({"success": False, "error": "Order not found"}), 404
        
        # Delete order items first
        OrderItem.query.filter_by(order_id=id).delete()
        
        # Delete order
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Order deleted successfully"
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
    PORT = 5003  # Nadia's Order Service
    print(f"Order Service starting on port {PORT}")
    print(f"🩺 Health Check: http://localhost:{PORT}/health")
    print(f"Available endpoints (4 HTTP methods):")
    print(f"   GET    /api/orders          - List all orders")
    print(f"   GET    /api/orders/<id>     - Get single order with items")
    print(f"   POST   /api/orders          - Create order (with items)")
    print(f"   PUT    /api/orders/<id>     - Update order (status, items, etc.)")
    print(f"   DELETE /api/orders/<id>     - Delete order")
    app.run(host='127.0.0.1', port=PORT, debug=True)