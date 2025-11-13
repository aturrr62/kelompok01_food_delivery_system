from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfigurasi database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================================
# MODEL
# ==========================================================
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    driver_name = db.Column(db.String(100))
    status = db.Column(db.String(50), default="pending")
    destination = db.Column(db.String(255))
    current_location = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "driver_name": self.driver_name,
            "status": self.status,
            "destination": self.destination,
            "current_location": self.current_location,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }

# ==========================================================
# DATABASE INIT
# ==========================================================
with app.app_context():
    db.create_all()

# ==========================================================
# ROUTES
# ==========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Delivery Service",
        "status": "active",
        "message": "Welcome to Delivery Microservice (port 5004)"
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"success": True, "message": "Delivery Service running on port 5004"}), 200

# CREATE
@app.route("/deliveries", methods=["POST"])
def create_delivery():
    data = request.get_json()
    if not data or "order_id" not in data:
        return jsonify({"success": False, "message": "order_id is required"}), 400

    new_delivery = Delivery(
        order_id=data["order_id"],
        driver_name=data.get("driver_name"),
        status=data.get("status", "pending"),
        destination=data.get("destination"),
        current_location=data.get("current_location")
    )
    db.session.add(new_delivery)
    db.session.commit()

    return jsonify({"success": True, "data": new_delivery.to_dict()}), 201

# READ ALL
@app.route("/deliveries", methods=["GET"])
def get_all_deliveries():
    include_deleted = request.args.get("include_deleted", "false").lower() == "true"
    if include_deleted:
        deliveries = Delivery.query.all()
    else:
        deliveries = Delivery.query.filter_by(is_active=True).all()

    return jsonify({
        "success": True,
        "count": len(deliveries),
        "data": [d.to_dict() for d in deliveries]
    }), 200

# READ BY ID
@app.route("/deliveries/<int:delivery_id>", methods=["GET"])
def get_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    return jsonify({"success": True, "data": delivery.to_dict()}), 200

# UPDATE
@app.route("/deliveries/<int:delivery_id>", methods=["PUT"])
def update_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    data = request.get_json()

    delivery.driver_name = data.get("driver_name", delivery.driver_name)
    delivery.status = data.get("status", delivery.status)
    delivery.destination = data.get("destination", delivery.destination)
    delivery.current_location = data.get("current_location", delivery.current_location)
    db.session.commit()

    return jsonify({"success": True, "message": "Delivery updated", "data": delivery.to_dict()}), 200

# SOFT DELETE
@app.route("/deliveries/<int:delivery_id>/soft-delete", methods=["DELETE"])
def soft_delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.is_active = False
    delivery.deleted_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"success": True, "message": "Delivery soft deleted"}), 200

# HARD DELETE
@app.route("/deliveries/<int:delivery_id>", methods=["DELETE"])
def hard_delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    db.session.delete(delivery)
    db.session.commit()
    return jsonify({"success": True, "message": "Delivery permanently deleted"}), 200

# RESTORE
@app.route("/deliveries/<int:delivery_id>/restore", methods=["POST"])
def restore_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.is_active = True
    delivery.deleted_at = None
    db.session.commit()
    return jsonify({"success": True, "message": "Delivery restored", "data": delivery.to_dict()}), 200

# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    app.run(port=5004, debug=True)
