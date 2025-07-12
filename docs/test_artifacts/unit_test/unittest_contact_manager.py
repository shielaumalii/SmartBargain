#Run as "python -m core.backend.unittest_contact_manager" to runa s a package and palce this unit tets file with the original file for the unit test file to work
import unittest
from core.backend.contact_manager import ContactManager

class TestContactManager(unittest.TestCase):

    def setUp(self):
        self.manager = ContactManager()
        self.test_name = "Test User"
        self.test_email = "testuser@example.com"
        self.test_message = "This is a test message."

    def test_save_message(self):
        self.manager.save_message(self.test_name, self.test_email, self.test_message)

    def test_get_all_messages(self):
        self.manager.get_messages()

    def test_get_messages_by_status(self):
        self.manager.get_messages(status="open")

    def test_get_messages_by_date(self):
        self.manager.get_messages(date="2025-07-01")

    def test_get_message_by_id(self):
        self.manager.get_message_by_id(1)

    def test_close_message(self):
        self.manager.close_message(1)

if __name__ == '__main__':
    unittest.main()
