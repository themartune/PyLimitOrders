import unittest
from limit.limit_order_agent import Exc, LimitOrderAgent


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self) -> None:
        # instantiate Execution Client
        self.e = Exc()

        # instantiate LimitOrderAgent
        self.loa = LimitOrderAgent(self.e)

    def test_loa_default_order_size(self):
        """instantiate the LimitOrderAgent and make sure that it has an empty order list"""
        self.assertTrue(len(self.loa.orders.items()) == 0)

    def test_add_orders_to_loa(self):
        """add a standard set of orders and make sure that the counts are correct"""
        self.add_orders()

        # test added orders
        self.assertTrue(len(self.loa.orders['IBM']) == 4)
        self.assertTrue(len(self.loa.orders['JBL']) == 1)
        self.assertTrue(len(self.loa.orders['HAL']) == 1)

        # test an order that isn't in the list
        self.assertTrue(len(self.loa.orders['BP']) == 0)

    def test_processing_orders(self):
        """Price IBM at 100
        1 should Sell
        1 should buy
        Other orders should remain untouched
        """
        self.add_orders()

        self.loa.on_price_tick('IBM', 100)

        self.assertTrue(len(self.loa.orders['IBM']) == 2)
        self.assertTrue(len(self.loa.orders['JBL']) == 1)
        self.assertTrue(len(self.loa.orders['HAL']) == 1)

    def add_orders(self):
        self.loa.add_order('IBM', 1000, 101, True)  # Buy
        self.loa.add_order('IBM', 1000, 99, True)  # Buy
        self.loa.add_order('IBM', 1000, 90, False)  # Sell
        self.loa.add_order('IBM', 1000, 105, False)  # Sell
        self.loa.add_order('JBL', 1000, 100, True)  # Buy
        self.loa.add_order('HAL', 1000, 100, False)  # Sell


if __name__ == '__main__':
    unittest.main()
