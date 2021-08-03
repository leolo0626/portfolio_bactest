import unittest
from src.Portfolio import Portfolio
from src.Order import Order
class Test1(unittest.TestCase):
    portfolio = Portfolio()

    def test_add_capital(self):
        self.portfolio.add_capital(1000000)
        self.assertEqual(1000000, self.portfolio.cash)
        self.assertEqual(1000000, self.portfolio.net_asset_value)

    def test_order_amount_calculation(self):
        buy_order = Order('700', 451.6, 500, 250, 'b')
        self.assertEqual(226050 ,buy_order.total_amount)
        sell_order = Order('700', 480.2, 500, 250, 's')
        self.assertEqual(239850, sell_order.total_amount)
    
    def test_add_long_position(self):
        first_buy_order  = Order('700', 451.6, 500, 250, 'b')
        self.portfolio.add_long_position(first_buy_order)
        self.assertEqual(1, self.portfolio.size)
        self.assertEqual(773950, self.portfolio.cash)
        self.assertDictEqual({
                '700' : {'ticker' : '700',
                'price' : 451.6,
                'shares' : 500,
                'total_cost' : 226050,
                'last_price' : None, 
                'market_value' : None, 
                'unrealized_pnl' : None, 
                'realized_pnl' : None}
        }, self.portfolio.positions)
    
    def test_cover_position(self) : 
        first_sell_order = Order('700',  480.2, 500, 250, 's')
        position = self.portfolio.cover_position(first_sell_order)
        self.assertEqual(0, self.portfolio.size)
        self.assertEqual(1013800, self.portfolio.cash)
        self.assertDictEqual({}, self.portfolio.positions)
        self.assertDictEqual( {
                'ticker' : '700',
                'price' : 451.6,
                'shares' : 0,
                'total_cost' : 226050,
                'last_price' : None, 
                'market_value' : None, 
                'unrealized_pnl' : None, 
                'realized_pnl' : 13800}, position)
    
    # def test_boolean(self):
    #     a = True
    #     b = False
    #     self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()