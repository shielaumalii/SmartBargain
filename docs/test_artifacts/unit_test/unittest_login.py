#Run as "python -m core.backend.unittest_login" to runa s a package and palce this unit tets file with the original file for the unit test file to work
import unittest
from core.backend.login import register_user, login_user

class TestLogin(unittest.TestCase):

    def test_register_user(self):
        register_user("Test User", "test1@example.com", "pass123", "buyer")

    def test_register_existing_user(self):
        register_user("Test User", "test2@example.com", "pass123", "seller")
        register_user("Test User", "test2@example.com", "pass123", "seller")

    def test_login_user(self):
        register_user("Test User", "test3@example.com", "pass123", "buyer")
        login_user("test3@example.com", "pass123")

    def test_login_invalid(self):
        login_user("invalid@example.com", "wrongpass")

if __name__ == '__main__':
    unittest.main()
