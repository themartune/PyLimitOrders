from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
from collections import defaultdict


class Exc(ExecutionClient):
    """Modified Execution Client with functional buy and sell routines"""
    def buy(self,
            product_id: str,
            quantity: int,
            price: float):

        try:
            print(f'Bought {quantity} shares of {product_id} at ${price}')

        except:  # this needs to have specific exceptions listed
            raise ExecutionException

        return True

    def sell(self,
             product_id: str,
             quantity: int,
             price: float):

        try:
            print(f'Sold {quantity} shares of {product_id} at ${price}')

        except:  # this needs to have specific exceptions listed too
            raise ExecutionException

        return True


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        Holds a list of orders and the code to add and process them
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.orders = defaultdict(list)
        # super().__init__()  # Protocols cannot be instantiated

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        """Calls processing routine based on the ticker symbol and price
        :param product_id: Ticker symbol to be processed
        :param price: price of the equity
        """
        print(f'Executing orders for {product_id} at {price}')
        self._process_orders(product_id, price)

    def add_order(self,
                  product_id: str,
                  quantity: float,
                  limit: float,
                  buy: bool,
                 ):
        self.orders[product_id].append({'buy': buy,
                                        'quantity': quantity,
                                        'limit': limit})

    def _process_orders(self,
                        product_id: str,
                        current_price: float):
        """Loop through order list associated with product_id and call buy or sell from the execution_client
        :param product_id: Ticker symbol to be processed
        :param current_price: price of the equity
        """
        successful_orders = []
        for i, order in enumerate(self.orders[product_id]):
            if order['limit'] <= current_price and order['buy']:
                if self.execution_client.buy(product_id, order['quantity'], current_price):
                    successful_orders.append(i)
            elif order['limit'] >= current_price and not order['buy']:
                if self.execution_client.sell(product_id, order['quantity'], current_price):
                    successful_orders.append(i)

        # remove successful orders from order list
        for idx in successful_orders[::-1]:
            del self.orders[product_id][idx]


if __name__ == '__main__':
    e = Exc()
    loa = LimitOrderAgent(e)

    loa.add_order('IBM', 1000, 100, True)
    loa.add_order('IBM', 1000, 100, True)
    loa.add_order('IBM', 1000, 100, False)
    loa.add_order('IBM', 1000, 105, False)
    loa.add_order('JBL', 1000, 100, True)
    loa.add_order('HAL', 1000, 100, False)

    print(len(loa.orders['IBM']), loa.orders['IBM'])

    loa.on_price_tick('IBM', 105.00)

    print(len(loa.orders['IBM']), loa.orders['IBM'])
