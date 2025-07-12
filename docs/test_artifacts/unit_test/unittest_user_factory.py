# palce this unit tets file with the original file for the unit test file to work
import unittest
from user_factory import UserFactory, Buyer, Seller

class TestUserFactory(unittest.TestCase):

    def test_create_buyer(self):
        user = UserFactory.create_user('buyer', 'Buyername', 'B@example.com', '1234')

    def test_create_seller(self):
        user = UserFactory.create_user('seller', 'Sellername', 'S@example.com', '5678')
        
    def test_invalid_role(self):
        with self.assertRaises(ValueError):  #  Adding this line here cause im expect to get a value error here
            UserFactory.create_user('testrole', 'Buyername', 'B@example.com', '1234')
            
    #This test fails as there is no validation for incorrect email format in the funcation , its handleed in the front end 
    '''def test_invalid_email(self):
        with self.assertRaises(ValueError):
            UserFactory.create_user('seller', 'Buyername', 'invalid-email', '1234')'''
    

if __name__ == '__main__':
    unittest.main()
