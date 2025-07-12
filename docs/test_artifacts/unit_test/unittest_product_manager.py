#Run as "python -m core.backend.unittest_product_managerr" to runa s a package and palce this unit tets file with the original file for the unit test file to work
import unittest
from core.backend.contact_manager import ContactManager

class TestContactManager(unittest.TestCase):

    def test_save_message(self):
        ContactManager().save_message("John Doe", "john@example.com", "Test message")

    def test_get_all_messages(self):
        ContactManager().get_messages()

    def test_get_messages_by_status(self):
        ContactManager().get_messages(status="open")

    def test_get_messages_by_date(self):
        ContactManager().get_messages(date="2024-12-31")

    def test_get_message_by_id(self):
        ContactManager().get_message_by_id(1)

    def test_close_message(self):
        ContactManager().close_message(1)

if __name__ == '__main__':
    unittest.main()
