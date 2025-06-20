class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

class Buyer(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, role='buyer')

class Seller(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, role='seller')

class UserFactory:
    @staticmethod
    def create_user(role, name, email, password):
        if role == 'buyer':
            return Buyer(name, email, password)
        elif role == 'seller':
            return Seller(name, email, password)
        else:
            raise ValueError("Invalid role selected")
