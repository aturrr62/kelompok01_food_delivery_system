from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delivery_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ========================
#  DELIVERY SERVICE MODELS
# ========================
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False, unique=True)
    courier_id = db.Column(db.Integer, nullable=True)
    courier_name = db.Column(db.String(100), nullable=True)
    courier_phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, assigned, picked_up, in_transit, delivered, cancelled
    pickup_address = db.Column(db.Text)
    delivery_address = db.Column(db.Text, nullable=False)
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    estimated_delivery_time = db.Column(db.DateTime, nullable=True)
    actual_delivery_time = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'courier_id': self.courier_id,
            'courier_name': self.courier_name,
            'courier_phone': self.courier_phone,
            'status': self.status,
            'pickup_address': self.pickup_address,
            'delivery_address': self.delivery_address,
            'current_location': {
                'latitude': self.current_latitude,
                'longitude': self.current_longitude
            } if self.current_latitude else None,
            'estimated_delivery_time': self.estimated_delivery_time.isoformat() if self.estimated_delivery_time else None,
            'actual_delivery_time': self.actual_delivery_time.isoformat() if self.actual_delivery_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def create_tables():
    with app.app_context():
        db.create_all()
        print("Delivery Service tables created")

# ========================
# CRUD ENDPOINTS (4 Methods)
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "delivery-service",
        "timestamp": datetime.utcnow().isoformat()
    })

# GET - List all deliveries
@app.route('/api/deliveries', methods=['GET'])
def get_all_deliveries():
    """GET - List all deliveries"""
    try:
        status = request.args.get('status')
        order_id = request.args.get('order_id', type=int)
        courier_id = request.args.get('courier_id', type=int)
        
        query = Delivery.query
        
        if status:
            query = query.filter_by(status=status)
        if order_id:
            query = query.filter_by(order_id=order_id)
        if courier_id:
            query = query.filter_by(courier_id=courier_id)
            
        deliveries = query.all()
        
        return jsonify({
            "success": True,
            "data": [delivery.to_dict() for delivery in deliveries],
            "count": len(deliveries)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET - Get single delivery by ID
@app.route('/api/deliveries/<int:id>', methods=['GET'])
def get_delivery(id):
    """GET - Get single delivery with tracking"""
    try:
        delivery = Delivery.query.get(id)
        if not delivery:
            return jsonify({"success": False, "error": "Delivery not found"}), 404
            
        return jsonify({
            "success": True,
            "data": delivery.to_dict()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# POST - Create new delivery
@app.route('/api/deliveries', methods=['POST'])
def create_delivery():
    """POST - Create new delivery"""
    try:
        data = request.get_json()
        
        if not data or not data.get('order_id') or not data.get('delivery_address'):
            return jsonify({"success": False, "error": "order_id and delivery_address are required"}), 400
        
        # Check if delivery for this order already exists
        existing = Delivery.query.filter_by(order_id=data['order_id']).first()
        if existing:
            return jsonify({"success": False, "error": "Delivery for this order already exists"}), 409
        
        new_delivery = Delivery(
            order_id=data['order_id'],
            delivery_address=data['delivery_address'],
            pickup_address=data.get('pickup_address'),
            courier_id=data.get('courier_id'),
            courier_name=data.get('courier_name'),
            courier_phone=data.get('courier_phone'),
            status=data.get('status', 'pending'),
            estimated_delivery_time=data.get('estimated_delivery_time'),
            notes=data.get('notes')
        )
        
        db.session.add(new_delivery)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": new_delivery.to_dict(),
            "message": "Delivery created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# PUT - Update delivery (assign courier, update location, change status)
@app.route('/api/deliveries/<int:id>', methods=['PUT'])
def update_delivery(id):
    """PUT - Update delivery (courier, location, status, etc.)"""
    try:
        delivery = Delivery.query.get(id)
        if not delivery:
            return jsonify({"success": False, "error": "Delivery not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update courier assignment
        if 'courier_id' in data:
            delivery.courier_id = data['courier_id']
        if 'courier_name' in data:
            delivery.courier_name = data['courier_name']
        if 'courier_phone' in data:
            delivery.courier_phone = data['courier_phone']
        
        # Update location
        if 'current_latitude' in data:
            delivery.current_latitude = float(data['current_latitude'])
        if 'current_longitude' in data:
            delivery.current_longitude = float(data['current_longitude'])
        
        # Update status
        if 'status' in data:
            delivery.status = data['status']
            
            # Auto-set actual delivery time when status becomes 'delivered'
            if data['status'] == 'delivered' and not delivery.actual_delivery_time:
                delivery.actual_delivery_time = datetime.utcnow()
        
        # Update other fields
        if 'pickup_address' in data:
            delivery.pickup_address = data['pickup_address']
        if 'delivery_address' in data:
            delivery.delivery_address = data['delivery_address']
        if 'estimated_delivery_time' in data:
            delivery.estimated_delivery_time = data['estimated_delivery_time']
        if 'notes' in data:
            delivery.notes = data['notes']
        
        delivery.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": delivery.to_dict(),
            "message": "Delivery updated successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE - Delete delivery
@app.route('/api/deliveries/<int:id>', methods=['DELETE'])
def delete_delivery(id):
    """DELETE - Delete delivery permanently"""
    try:
        delivery = Delivery.query.get(id)
        if not delivery:
            return jsonify({"success": False, "error": "Delivery not found"}), 404
        
        db.session.delete(delivery)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Delivery deleted successfully"
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
    PORT = 5004  # aydin's Delivery Service
    print(f"🚚 Delivery Service starting on port {PORT}")
    print(f"🩺 Health Check: http://localhost:{PORT}/health")
    print(f"Available endpoints (4 HTTP methods):")
    print(f"   GET    /api/deliveries          - List all deliveries")
    print(f"   GET    /api/deliveries/<id>     - Get delivery with tracking")
    print(f"   POST   /api/deliveries          - Create delivery")
    print(f"   PUT    /api/deliveries/<id>     - Update delivery (courier, location, status)")
    print(f"   DELETE /api/deliveries/<id>     - Delete delivery")
    app.run(host='127.0.0.1', port=PORT, debug=True)