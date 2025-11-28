PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS delivery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL UNIQUE,
    courier_id INTEGER,
    courier_name TEXT,
    courier_phone TEXT,
    status TEXT DEFAULT 'pending',
    pickup_address TEXT NOT NULL,
    delivery_address TEXT NOT NULL,
    estimated_pickup_time TEXT,
    actual_pickup_time TEXT,
    estimated_delivery_time TEXT,
    actual_delivery_time TEXT,
    current_latitude REAL,
    current_longitude REAL,
    delivery_fee REAL DEFAULT 0.0,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS courier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    vehicle_type TEXT NOT NULL,
    vehicle_number TEXT,
    license_number TEXT,
    current_latitude REAL,
    current_longitude REAL,
    status TEXT DEFAULT 'available',
    rating REAL DEFAULT 5.0,
    total_deliveries INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS delivery_location_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id INTEGER NOT NULL,
    courier_id INTEGER,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    status TEXT,
    notes TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(delivery_id) REFERENCES delivery(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_delivery_status ON delivery(status);
CREATE INDEX IF NOT EXISTS idx_courier_status ON courier(status);
CREATE INDEX IF NOT EXISTS idx_location_delivery_id ON delivery_location_history(delivery_id);

