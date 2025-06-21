from .database import create_connection

class ProductManager:

    @staticmethod
    def get_all_products():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    @staticmethod
    def add_product(name, image_url, quantity, price, per, category, seller_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, image_url, quantity, price, per, category, seller_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, image_url, quantity, price, per, category, seller_id))
        conn.commit()

    @staticmethod
    def update_product(product_id, quantity, price, per):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET quantity = ?, price = ?, per = ?
            WHERE id = ?
        """, (quantity, price, per, product_id))
        conn.commit()

    @staticmethod
    def delete_product(product_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()

    @staticmethod
    def purchase_product(product_id, quantity):
        conn = create_connection()
        cursor = conn.cursor()

        # Check current stock
        cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Product not found"

        current_qty = row[0]
        if current_qty < quantity:
            return False, "Insufficient stock"

        # Reduce quantity
        new_qty = current_qty - quantity
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))
        conn.commit()
        return True, "Purchase successful"
