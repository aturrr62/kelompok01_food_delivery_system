from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ========================
#  PAYMENT SERVICE MODELS
# ========================
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, debit_card, ewallet, bank_transfer, cod
    status = db.Column(db.String(20), default='pending')  # pending, processing, success, failed, refunded
    card_last_4 = db.Column(db.String(4), nullable=True)
    notes = db.Column(db.Text)
    refund_amount = db.Column(db.Float, default=0.0)
    refund_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'card_last_4': self.card_last_4,
            'notes': self.notes,
            'refund_amount': self.refund_amount,
            'refund_reason': self.refund_reason,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def create_tables():
    with app.app_context():
        db.create_all()
        print("Payment Service tables created")

def generate_transaction_id():
    return f"TXN-{uuid.uuid4().hex[:16].upper()}"

def simulate_payment_processing(amount, method):
    """Simulate payment gateway - 90% success rate"""
    success = random.random() < 0.9
    return {
        'success': success,
        'message': 'Payment processed successfully' if success else 'Payment failed',
        'gateway_response': f"Gateway-{random.randint(1000, 9999)}"
    }

# ========================
# CRUD ENDPOINTS (4 Methods)
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "payment-service",
        "timestamp": datetime.utcnow().isoformat()
    })

# GET - List all payments
@app.route('/api/payments', methods=['GET'])
def get_all_payments():
    """GET - List all payments"""
    try:
        user_id = request.args.get('user_id', type=int)
        order_id = request.args.get('order_id', type=int)
        status = request.args.get('status')
        
        query = Payment.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if order_id:
            query = query.filter_by(order_id=order_id)
        if status:
            query = query.filter_by(status=status)
            
        payments = query.all()
        
        return jsonify({
            "success": True,
            "data": [payment.to_dict() for payment in payments],
            "count": len(payments)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET - Get single payment by ID
@app.route('/api/payments/<int:id>', methods=['GET'])
def get_payment(id):
    """GET - Get single payment"""
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({"success": False, "error": "Payment not found"}), 404
            
        return jsonify({
            "success": True,
            "data": payment.to_dict()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# POST - Create new payment (auto-process)
@app.route('/api/payments', methods=['POST'])
def create_payment():
    """POST - Create and process payment"""
    try:
        data = request.get_json()
        
        required_fields = ['order_id', 'user_id', 'amount', 'payment_method']
        for field in required_fields:
            if not data or not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Create payment
        new_payment = Payment(
            order_id=data['order_id'],
            user_id=data['user_id'],
            transaction_id=generate_transaction_id(),
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            card_last_4=data.get('card_last_4'),
            notes=data.get('notes'),
            status='processing'
        )
        
        db.session.add(new_payment)
        db.session.flush()
        
        # Auto-process payment (simulate gateway)
        auto_process = data.get('auto_process', True)
        
        if auto_process:
            gateway_response = simulate_payment_processing(new_payment.amount, new_payment.payment_method)
            
            if gateway_response['success']:
                new_payment.status = 'success'
                new_payment.notes = f"{new_payment.notes or ''} | Gateway: {gateway_response['gateway_response']}"
            else:
                new_payment.status = 'failed'
                new_payment.notes = f"{new_payment.notes or ''} | Failed: {gateway_response['message']}"
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": new_payment.to_dict(),
            "message": "Payment created and processed"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# PUT - Update payment (process, refund, change status)
@app.route('/api/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    """PUT - Update payment (process or refund)"""
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({"success": False, "error": "Payment not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        action = data.get('action', 'update')  # update, process, refund
        
        # REFUND ACTION
        if action == 'refund':
            if payment.status != 'success':
                return jsonify({"success": False, "error": "Only successful payments can be refunded"}), 400
            
            refund_amount = float(data.get('refund_amount', payment.amount))
            
            if refund_amount > payment.amount:
                return jsonify({"success": False, "error": "Refund amount cannot exceed payment amount"}), 400
            
            payment.refund_amount = refund_amount
            payment.refund_reason = data.get('refund_reason', '')
            payment.status = 'refunded'
            
        # PROCESS ACTION
        elif action == 'process':
            if payment.status not in ['pending', 'failed']:
                return jsonify({"success": False, "error": "Payment already processed"}), 400
            
            gateway_response = simulate_payment_processing(payment.amount, payment.payment_method)
            
            if gateway_response['success']:
                payment.status = 'success'
                payment.notes = f"{payment.notes or ''} | Gateway: {gateway_response['gateway_response']}"
            else:
                payment.status = 'failed'
                payment.notes = f"{payment.notes or ''} | Failed: {gateway_response['message']}"
        
        # REGULAR UPDATE
        else:
            if 'status' in data:
                payment.status = data['status']
            if 'payment_method' in data:
                payment.payment_method = data['payment_method']
            if 'notes' in data:
                payment.notes = data['notes']
            if 'card_last_4' in data:
                payment.card_last_4 = data['card_last_4']
        
        payment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": payment.to_dict(),
            "message": f"Payment {action}d successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE - Delete payment
@app.route('/api/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    """DELETE - Delete payment permanently"""
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({"success": False, "error": "Payment not found"}), 404
        
        db.session.delete(payment)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Payment deleted successfully"
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
    PORT = 5005  # reza's Payment Service
    print(f"💳 Payment Service starting on port {PORT}")
    print(f"🩺 Health Check: http://localhost:{PORT}/health")
    print(f"Available endpoints (4 HTTP methods):")
    print(f"   GET    /api/payments          - List all payments")
    print(f"   GET    /api/payments/<id>     - Get single payment")
    print(f"   POST   /api/payments          - Create payment (auto-process)")
    print(f"   PUT    /api/payments/<id>     - Update payment (process/refund via action parameter)")
    print(f"   DELETE /api/payments/<id>     - Delete payment")
    app.run(host='127.0.0.1', port=PORT, debug=True)