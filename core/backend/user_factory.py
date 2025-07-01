class User:
    def __init__(self, name, email, password, role, user_id=None):
        self.id = user_id  # Add user_id support
        self.name = name
        self.email = email
        self.password = password
        self.role = role

class Buyer(User):
    def __init__(self, name, email, password, user_id=None):
        super().__init__(name, email, password, role='buyer', user_id=user_id)

class Seller(User):
    def __init__(self, name, email, password, user_id=None):
        super().__init__(name, email, password, role='seller', user_id=user_id)

class UserFactory:
    @staticmethod
    def create_user(role, name, email, password, user_id=None):
        if role == 'buyer':
            return Buyer(name, email, password, user_id)
        elif role == 'seller':
            return Seller(name, email, password, user_id)
        else:
            raise ValueError("Invalid role selected")

