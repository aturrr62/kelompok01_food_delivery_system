PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    transaction_id TEXT NOT NULL UNIQUE,
    payment_method TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'IDR',
    status TEXT DEFAULT 'pending',
    payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
    expiry_date TEXT,
    gateway_response TEXT,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS payment_method (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    card_number_hash TEXT,
    card_holder_name TEXT,
    expiry_month INTEGER,
    expiry_year INTEGER,
    cvv_hash TEXT,
    provider TEXT,
    is_default INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS payment_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    status_before TEXT,
    status_after TEXT NOT NULL,
    amount_before REAL,
    amount_after REAL,
    notes TEXT,
    gateway_data TEXT,
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(payment_id) REFERENCES payment(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS refund (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    refund_amount REAL NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    processed_date TEXT,
    refund_transaction_id TEXT,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(payment_id) REFERENCES payment(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_payment_status ON payment(status);
CREATE INDEX IF NOT EXISTS idx_payment_user ON payment(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_order ON payment(order_id);
CREATE INDEX IF NOT EXISTS idx_payment_method_user ON payment_method(user_id);

