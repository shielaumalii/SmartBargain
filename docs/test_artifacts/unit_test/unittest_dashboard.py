#Run as "python -m core.backend.unittest_dashboard" to runa s a package and palce this unit tets file with the original file for the unit test file to work
import unittest
from core.backend import dashboard  # adjust if your filename is different

class TestDashboard(unittest.TestCase):

    def test_get_negotiation_tasks_buyer(self):
        dashboard.get_negotiation_tasks("buyer@example.com", "buyer")

    def test_get_negotiation_tasks_seller(self):
        dashboard.get_negotiation_tasks("seller@example.com", "seller")

    def test_update_negotiation_status(self):
        dashboard.update_negotiation_status_in_db(1, "Active")

    def test_save_negotiation_response(self):
        dashboard.save_negotiation_response(1, 5, 10.0, "test", "accept")

    def test_get_orders_for_user_id(self):
        dashboard.get_orders_for_user_id(1)

    def test_get_orders_for_seller(self):
        dashboard.get_orders_for_seller(1)

    def test_get_negotiation_dashboard_data_buyer(self):
        dashboard.get_negotiation_dashboard_data(1, "buyer")

    def test_get_negotiation_dashboard_data_seller(self):
        dashboard.get_negotiation_dashboard_data(1, "seller")

    def test_update_negotiation_dashboard_response(self):
        dashboard.update_negotiation_dashboard_response(1, 5, 12.0, "counter offer", "counter")

if __name__ == '__main__':
    unittest.main()
