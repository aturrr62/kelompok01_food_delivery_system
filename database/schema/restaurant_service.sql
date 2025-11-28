PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    phone TEXT,
    email TEXT,
    rating REAL DEFAULT 0.0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS menu_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT,
    image_url TEXT,
    is_available INTEGER DEFAULT 1,
    is_vegetarian INTEGER DEFAULT 0,
    is_spicy INTEGER DEFAULT 0,
    preparation_time INTEGER,
    calories INTEGER,
    allergens TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT,
    FOREIGN KEY(restaurant_id) REFERENCES restaurant(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_menu_item_restaurant_id ON menu_item(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_menu_item_category ON menu_item(category);

