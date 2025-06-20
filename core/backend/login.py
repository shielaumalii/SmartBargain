from .user_factory import UserFactory
from .database import DatabaseConnection, create_tables

def register_user(name, email, password, role):
    user = UserFactory.create_user(role, name, email, password)
    conn = DatabaseConnection.get_instance()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
        if cursor.fetchone():
            return False, "User already exists with this email."

        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", 
                       (user.name, user.email, user.password, user.role))
        conn.commit()
        return True, f"{user.role.capitalize()} registered successfully!"
    except Exception as e:
        return False, f"Error: {e}"

def login_user(email, password):
    conn = DatabaseConnection.get_instance()
    cursor = conn.cursor()
    cursor.execute("SELECT name, role FROM users WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()

    if result:
        user = {"name": result[0], "role": result[1], "email": email}
        return True, user
    else:
        return False, "Login failed. Please check your credentials."
