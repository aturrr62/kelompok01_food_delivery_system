"""
Database Migration Script - Food Delivery System
Adds missing columns to Order and Payment tables safely
"""

import sqlite3
import os
from pathlib import Path

# Base path
BASE_DIR = Path(__file__).parent / "microservices"

def migrate_order_service():
    """Add total_price column to Order table"""
    db_path = BASE_DIR / "order-service" / "order_service.db"
    
    if not db_path.exists():
        print(f" Order Service database not found: {db_path}")
        print("   Database will be created when service starts.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info('order')")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'total_price' in columns:
            print("Order Service: total_price column already exists")
            return True
        
        # Add column
        print("Order Service: Adding total_price column...")
        cursor.execute("ALTER TABLE 'order' ADD COLUMN total_price REAL DEFAULT 0.0")
        conn.commit()
        
        print("Order Service: Migration successful!")
        conn.close()
        return True
        
    except Exception as e:
        print(f"Order Service migration failed: {e}")
        return False

def migrate_payment_service():
    """Add card_last_4 column to Payment table"""
    db_path = BASE_DIR / "payment-service" / "payment_service.db"
    
    if not db_path.exists():
        print(f" Payment Service database not found: {db_path}")
        print("   Database will be created when service starts.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(payment)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'card_last_4' in columns:
            print("Payment Service: card_last_4 column already exists")
            return True
        
        # Add column
        print("Payment Service: Adding card_last_4 column...")
        cursor.execute("ALTER TABLE payment ADD COLUMN card_last_4 VARCHAR(4)")
        conn.commit()
        
        print("Payment Service: Migration successful!")
        conn.close()
        return True
        
    except Exception as e:
        print(f"Payment Service migration failed: {e}")
        return False

def main():
    print("=" * 60)
    print("  DATABASE MIGRATION - Food Delivery System")
    print("=" * 60)
    print()
    
    # Migrate Order Service
    print("Migrating Order Service...")
    order_success = migrate_order_service()
    print()
    
    # Migrate Payment Service
    print("💳 Migrating Payment Service...")
    payment_success = migrate_payment_service()
    print()
    
    # Summary
    print("=" * 60)
    print("  MIGRATION SUMMARY")
    print("=" * 60)
    
    if order_success and payment_success:
        print("All migrations completed successfully!")
        print()
        print("Next steps:")
        print("   1. Restart Order Service (port 5003)")
        print("   2. Restart Payment Service (port 5005)")
        print("   3. Test with Postman")
    else:
        print(" Some migrations failed or databases don't exist yet.")
        print()
        print("Recommended action:")
        print("   1. Stop all services")
        print("   2. Delete old database files")
        print("   3. Restart services (will create fresh databases)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
