# Run as "python -m core.backend.unittest_bargain_factory"to run as a package and palce this unit tets file with the original file for the unit test file to work
import unittest
from core.backend.bargain_factory import BargainFactory

class TestBargainFactory(unittest.TestCase):

    def test_create_setting(self):
        BargainFactory.create_setting(1, 10, 5.0).save()

    def test_create_request(self):
        BargainFactory.create_request(1, 1, 5, 4.5).save()

if __name__ == '__main__':
    unittest.main()
