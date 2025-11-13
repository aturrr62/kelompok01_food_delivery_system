from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfigurasi database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================================
# MODEL
# ==========================================================
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(50), default="pending")  # pending, success, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

with app.app_context():
    db.create_all()

# ==========================================================
# ROUTES
# ==========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Payment Service",
        "status": "active",
        "message": "Welcome to Payment Microservice (port 5005)"
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"success": True, "message": "Payment Service running on port 5005"}), 200

# CREATE
@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json()
    new_payment = Payment(
        order_id=data.get("order_id"),
        amount=data.get("amount"),
        payment_method=data.get("payment_method", "cash"),
        status=data.get("status", "pending")
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"success": True, "data": new_payment.to_dict()}), 201

# READ ALL
@app.route("/payments", methods=["GET"])
def get_payments():
    payments = Payment.query.all()
    return jsonify({"success": True, "count": len(payments), "data": [p.to_dict() for p in payments]}), 200

# READ BY ID
@app.route("/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify({"success": True, "data": payment.to_dict()}), 200

# UPDATE STATUS
@app.route("/payments/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    payment.status = data.get("status", payment.status)
    db.session.commit()
    return jsonify({"success": True, "message": "Payment updated", "data": payment.to_dict()}), 200

# DELETE
@app.route("/payments/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({"success": True, "message": "Payment deleted"}), 200

# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    app.run(port=5005, debug=True)
