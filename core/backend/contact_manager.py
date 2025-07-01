from .database import create_connection

class ContactManager:
    def __init__(self):
        self.db  = create_connection()

    def get_messages(self, status=None, date=None):
        cursor = self.db.cursor()
        query = """
            SELECT id, name, email, message, status, created_at 
            FROM contact_messages
        """
        params = []
        conditions = []

        if status and status.lower() != 'all':
            conditions.append("status = ?")
            params.append(status)

        if date:
            conditions.append("DATE(created_at) = DATE(?)")
            params.append(date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        cursor.execute(query, params)
        return cursor.fetchall()


    def get_message_by_id(self, msg_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, name, email, message, status, created_at 
            FROM contact_messages 
            WHERE id = ?
        """, (msg_id,))
        return cursor.fetchone()

    def close_message(self, msg_id):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE contact_messages SET status = 'closed' WHERE id = ?
        """, (msg_id,))
        self.db.commit()

    def save_message(self, name, email, message):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (name, email, message)
            VALUES (?, ?, ?)
        """, (name, email, message))
        self.db.commit()
