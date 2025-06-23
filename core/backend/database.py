import os
import sqlite3

class DatabaseConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            # Ensures the DB is saved inside a folder called 'db' in the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_folder = os.path.join(base_dir, 'db')
            os.makedirs(db_folder, exist_ok=True)
            db_path = os.path.join(db_folder, 'smartbargain.db')

            DatabaseConnection._instance = sqlite3.connect(db_path, check_same_thread=False)
        return DatabaseConnection._instance

def create_connection():
    return DatabaseConnection.get_instance()

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
        # Drop tables if they exist (order matters due to foreign keys)
    cursor.execute("DROP TABLE IF EXISTS bargain_requests")
    cursor.execute("DROP TABLE IF EXISTS bargain_settings")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS users")



    # Users table (Buyer or Seller)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('buyer', 'seller'))
        )
    ''')

    # Products table
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS products (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_url TEXT,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                per TEXT NOT NULL,
                unit TEXT DEFAULT 'kg',
                category TEXT NOT NULL,
                seller_id INTEGER,
                FOREIGN KEY(seller_id) REFERENCES users(id)
        )
    ''')

    # Seller's bargain settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bargain_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL,
            min_price REAL NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Customer's bargain requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bargain_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    # Singleton, so no close here

if __name__ == "__main__":
    create_tables()
    print("Tables created!")