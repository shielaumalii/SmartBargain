from core.backend.database import create_connection

class BargainSetting:
    def __init__(self, product_id, min_quantity, min_price, unit="kg"):
        self.product_id = product_id
        self.min_quantity = min_quantity
        self.min_price = min_price
        

    def save(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO bargain_settings (product_id, min_quantity, min_price) VALUES (?, ?, ?)",
            (self.product_id, self.min_quantity, self.min_price)
        )
        conn.commit()

class BargainRequest:
    def __init__(self, product_id, user_id, quantity, price):
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.price = price

    def save(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bargain_requests (product_id, user_id, quantity, price) VALUES (?, ?, ?, ?)",
            (self.product_id, self.user_id, self.quantity, self.price)
        )
        conn.commit()

class BargainFactory:
    @staticmethod
    def create_setting(product_id, min_quantity, min_price):
        return BargainSetting(product_id, min_quantity, min_price)

    @staticmethod
    def create_request(product_id, user_id, quantity, price):
        return BargainRequest(product_id, user_id, quantity, price)