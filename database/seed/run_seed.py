"""
Utility script untuk membuat ulang seluruh database SQLite dan mengisi seed data.

Penggunaan:
    python database/seed/run_seed.py
"""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict

ROOT_DIR = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT_DIR / "database" / "schema"


def hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def iso_now(minutes_offset: int = 0) -> str:
    return (datetime.utcnow() + timedelta(minutes=minutes_offset)).isoformat()


def seed_user_service(conn: sqlite3.Connection) -> None:
    now = iso_now()
    cursor = conn.cursor()

    users = [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@fooddelivery.com",
            "password": "admin123",
            "full_name": "Admin FoodDelivery",
            "phone": "081111111111",
            "address": "Jl. Proyek No. 1, Jakarta",
            "user_type": "admin",
        },
        {
            "id": 2,
            "username": "user",
            "email": "user@fooddelivery.com",
            "password": "user123",
            "full_name": "Customer Demo",
            "phone": "082222222222",
            "address": "Jl. Proyek No. 2, Jakarta",
            "user_type": "customer",
        },
    ]

    for item in users:
        cursor.execute(
            """
            INSERT INTO user (
                id, username, email, password_hash, full_name, phone, address,
                user_type, is_active, created_at, updated_at, deleted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, NULL)
            """,
            (
                item["id"],
                item["username"],
                item["email"],
                hash_password(item["password"]),
                item["full_name"],
                item["phone"],
                item["address"],
                item["user_type"],
                now,
                now,
            ),
        )

    profiles = [
        {
            "user_id": 1,
            "bio": "Administrator sistem Food Delivery.",
            "date_of_birth": "1990-01-01",
            "preferences": '{"favorite_cuisine": "Indonesia"}',
            "avatar_url": "https://via.placeholder.com/128?text=Admin",
        },
        {
            "user_id": 2,
            "bio": "Pengguna demo untuk kebutuhan testing.",
            "date_of_birth": "1995-05-05",
            "preferences": '{"favorite_cuisine": "Padang"}',
            "avatar_url": "https://via.placeholder.com/128?text=User",
        },
    ]

    for profile in profiles:
        cursor.execute(
            """
            INSERT INTO user_profile (
                user_id, bio, date_of_birth, preferences, avatar_url,
                created_at, updated_at, deleted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
            """,
            (
                profile["user_id"],
                profile["bio"],
                profile["date_of_birth"],
                profile["preferences"],
                profile["avatar_url"],
                now,
                now,
            ),
        )


def seed_restaurant_service(conn: sqlite3.Connection) -> None:
    now = iso_now()
    cursor = conn.cursor()

    restaurants = [
        {
            "id": 1,
            "name": "Warung Bakso Malang",
            "description": "Bakso Malang autentik dengan kuah gurih.",
            "address": "Jl. Bakso No. 10, Jakarta",
            "phone": "021-123456",
            "email": "info@bakso-malang.com",
            "rating": 4.7,
        },
        {
            "id": 2,
            "name": "Nasi Goreng Nusantara",
            "description": "Spesialis nasi goreng khas daerah.",
            "address": "Jl. Nusantara No. 88, Bandung",
            "phone": "022-654321",
            "email": "halo@nasgor.com",
            "rating": 4.5,
        },
    ]

    for rest in restaurants:
        cursor.execute(
            """
            INSERT INTO restaurant (
                id, name, description, address, phone, email, rating,
                is_active, created_at, updated_at, deleted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, NULL)
            """,
            (
                rest["id"],
                rest["name"],
                rest["description"],
                rest["address"],
                rest["phone"],
                rest["email"],
                rest["rating"],
                now,
                now,
            ),
        )

    menu_items = [
        {
            "restaurant_id": 1,
            "name": "Bakso Urat Jumbo",
            "description": "Bakso urat ukuran jumbo dengan sambal mantap.",
            "price": 25000,
            "category": "main",
            "is_spicy": 1,
        },
        {
            "restaurant_id": 1,
            "name": "Mie Ayam Malang",
            "description": "Mie ayam gurih dengan pangsit.",
            "price": 20000,
            "category": "main",
            "is_spicy": 0,
        },
        {
            "restaurant_id": 2,
            "name": "Nasi Goreng Kampung",
            "description": "Nasi goreng dengan bumbu rempah kampung.",
            "price": 30000,
            "category": "main",
            "is_spicy": 1,
        },
        {
            "restaurant_id": 2,
            "name": "Teh Tarik Dingin",
            "description": "Teh tarik segar untuk menemani makan.",
            "price": 15000,
            "category": "drink",
            "is_spicy": 0,
        },
    ]

    for item in menu_items:
        cursor.execute(
            """
            INSERT INTO menu_item (
                restaurant_id, name, description, price, category, image_url,
                is_available, is_vegetarian, is_spicy, preparation_time,
                calories, allergens, is_active, created_at, updated_at, deleted_at
            )
            VALUES (?, ?, ?, ?, ?, NULL, 1, 0, ?, 15, 450, '[]', 1, ?, ?, NULL)
            """,
            (
                item["restaurant_id"],
                item["name"],
                item["description"],
                item["price"],
                item["category"],
                item["is_spicy"],
                now,
                now,
            ),
        )


def seed_order_service(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    created = iso_now(-30)
    delivered = iso_now(-5)

    cursor.execute(
        """
        INSERT INTO "order" (
            id, user_id, restaurant_id, order_number, status, total_amount,
            delivery_address, delivery_fee, special_instructions,
            estimated_delivery_time, actual_delivery_time, is_active,
            created_at, updated_at, deleted_at
        )
        VALUES (1, 2, 1, 'ORD-SEED-0001', 'delivered', 80000,
                'Jl. Testing No. 123, Jakarta', 5000, 'No sambal',
                ?, ?, 1, ?, ?, NULL)
        """,
        (iso_now(-15), delivered, created, delivered),
    )

    cursor.executemany(
        """
        INSERT INTO order_item (
            order_id, menu_item_id, menu_item_name, quantity,
            unit_price, total_price, special_requests,
            created_at, updated_at, deleted_at
        )
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
        """,
        [
            (1, "Bakso Urat Jumbo", 2, 25000, 50000, "", created, created),
            (2, "Mie Ayam Malang", 1, 20000, 20000, "Extra pangsit", created, created),
        ],
    )

    cursor.execute(
        """
        INSERT INTO order_status_history (
            order_id, old_status, new_status, notes, updated_by, created_at
        )
        VALUES
        (1, NULL, 'pending', 'Order dibuat', 2, ?),
        (1, 'pending', 'preparing', 'Sedang dimasak', 2, ?),
        (1, 'preparing', 'delivered', 'Pesanan sampai', 2, ?)
        """,
        (created, iso_now(-20), delivered),
    )


def seed_delivery_service(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    now = iso_now()

    couriers = [
        ("Rizky Kurir", "081234560001", "rizky@kurir.com", "motorcycle", "B 1234 XYZ", "SIM12345"),
        ("Siti Courier", "081234560002", "siti@kurir.com", "motorcycle", "B 9876 XYZ", "SIM67890"),
    ]
    for name, phone, email, vehicle, plate, license in couriers:
        cursor.execute(
            """
            INSERT INTO courier (
                name, phone, email, vehicle_type, vehicle_number, license_number,
                current_latitude, current_longitude, status, rating,
                total_deliveries, is_active, created_at, updated_at, deleted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, -6.2, 106.8, 'available', 4.9, 120, 1, ?, ?, NULL)
            """,
            (name, phone, email, vehicle, plate, license, now, now),
        )

    cursor.execute(
        """
        INSERT INTO delivery (
            id, order_id, courier_id, courier_name, courier_phone, status,
            pickup_address, delivery_address, estimated_pickup_time,
            actual_pickup_time, estimated_delivery_time, actual_delivery_time,
            current_latitude, current_longitude, delivery_fee, notes,
            is_active, created_at, updated_at, deleted_at
        )
        VALUES (
            1, 1, 1, 'Rizky Kurir', '081234560001', 'delivered',
            'Warung Bakso Malang, Jakarta',
            'Jl. Testing No. 123, Jakarta',
            ?, ?, ?, ?, -6.18, 106.82, 12000,
            'Sudah diterima pelanggan', 1, ?, ?, NULL
        )
        """,
        (iso_now(-25), iso_now(-20), iso_now(-10), iso_now(-5), now, now),
    )

    cursor.execute(
        """
        INSERT INTO delivery_location_history (
            delivery_id, courier_id, latitude, longitude, status, notes, timestamp
        )
        VALUES
        (1, 1, -6.190, 106.820, 'picked_up', 'Paket diambil', ?),
        (1, 1, -6.185, 106.825, 'in_transit', 'Sedang di perjalanan', ?),
        (1, 1, -6.180, 106.830, 'delivered', 'Pesanan diterima', ?)
        """,
        (iso_now(-20), iso_now(-12), iso_now(-5)),
    )


def seed_payment_service(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    now = iso_now()

    cursor.executemany(
        """
        INSERT INTO payment_method (
            id, user_id, name, card_number_hash, card_holder_name,
            expiry_month, expiry_year, cvv_hash, provider,
            is_default, is_active, created_at, updated_at, deleted_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, NULL)
        """,
        [
            (
                1,
                2,
                "BCA Virtual Account",
                hash_password("1234567890"),
                "Customer Demo",
                None,
                None,
                None,
                "bca",
                1,
                now,
                now,
            ),
            (
                2,
                2,
                "OVO Wallet",
                hash_password("ovo-demo-account"),
                "Customer Demo",
                None,
                None,
                None,
                "ovo",
                0,
                now,
                now,
            ),
        ],
    )

    cursor.execute(
        """
        INSERT INTO payment (
            id, order_id, user_id, transaction_id, payment_method, amount,
            currency, status, payment_date, expiry_date, gateway_response,
            notes, is_active, created_at, updated_at, deleted_at
        )
        VALUES (
            1, 1, 2, 'TXN-SEED-0001', 'bank_transfer', 80000,
            'IDR', 'completed', ?, NULL, '{"status":"completed"}',
            'Pembayaran sukses untuk order seed', 1, ?, ?, NULL
        )
        """,
        (now, now, now),
    )

    cursor.execute(
        """
        INSERT INTO payment_history (
            payment_id, action, status_before, status_after,
            amount_before, amount_after, notes, gateway_data,
            created_by, created_at
        )
        VALUES (
            1, 'completed', 'pending', 'completed',
            0, 80000, 'Pembayaran selesai', '{"code":"00"}',
            2, ?
        )
        """,
        (now,),
    )


ServiceConfig = Dict[str, Dict[str, object]]

SERVICES: ServiceConfig = {
    "user-service": {
        "db_path": ROOT_DIR / "microservices" / "user-service" / "instance" / "user_service.db",
        "schema": SCHEMA_DIR / "user_service.sql",
        "seed_func": seed_user_service,
    },
    "restaurant-service": {
        "db_path": ROOT_DIR / "microservices" / "restaurant-service" / "instance" / "restaurant.db",
        "schema": SCHEMA_DIR / "restaurant_service.sql",
        "seed_func": seed_restaurant_service,
    },
    "order-service": {
        "db_path": ROOT_DIR / "microservices" / "order-service" / "instance" / "order_service.db",
        "schema": SCHEMA_DIR / "order_service.sql",
        "seed_func": seed_order_service,
    },
    "delivery-service": {
        "db_path": ROOT_DIR / "microservices" / "delivery-service" / "instance" / "delivery_service.db",
        "schema": SCHEMA_DIR / "delivery_service.sql",
        "seed_func": seed_delivery_service,
    },
    "payment-service": {
        "db_path": ROOT_DIR / "microservices" / "payment-service" / "instance" / "payment_service.db",
        "schema": SCHEMA_DIR / "payment_service.sql",
        "seed_func": seed_payment_service,
    },
}


def recreate_database(name: str, config: Dict[str, object]) -> None:
    db_path: Path = config["db_path"]  # type: ignore[assignment]
    schema_path: Path = config["schema"]  # type: ignore[assignment]
    seed_func: Callable[[sqlite3.Connection], None] = config["seed_func"]  # type: ignore[assignment]

    print(f"\n🧹 Menghapus database lama untuk {name} ...")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    print(f"🧱 Menulis schema {schema_path.name} ...")
    conn = sqlite3.connect(db_path)
    with schema_path.open("r", encoding="utf-8") as schema_file:
        conn.executescript(schema_file.read())

    print(f"🌱 Menanam data awal untuk {name} ...")
    seed_func(conn)

    conn.commit()
    conn.close()
    print(f"Selesai untuk {name} ({db_path})")


def main() -> None:
    print("========================================")
    print("  Database Seeder - Food Delivery System ")
    print("========================================")

    for service_name, config in SERVICES.items():
        recreate_database(service_name, config)

    print("\nSemua database berhasil dibuat ulang dan di-seed!")


if __name__ == "__main__":
    main()

