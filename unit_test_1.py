import unittest
from src.Portfolio import Portfolio
from src.Order import Order
from src.DataLibrary import DataLibrary
import pandas as pd

class Test1(unittest.TestCase):
    portfolio = Portfolio()
    data_library = DataLibrary()

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
    
    def test_add_files_to_data_library(self) : 
        stock_price = pd.read_csv('test_files/2382_HK.csv')
        self.data_library.add_stock_price_library('2382', stock_price)
        self.assertEqual(['2382'], list(self.data_library.stock_price_library.keys()))

    def test_monitor_sell_cond(self) : 
        new_order = Order('2382', 170, 500, 0, 'b')
        self.portfolio.add_long_position(new_order)
        self.assertEqual(1, self.portfolio.size)
        self.assertEqual(['2382'], list(self.portfolio.positions.keys()))
        def sell_condition(ticker, date_time, data_library):
            #User defined functions
            # Input : dataframe , date_time in yyyy-mm-dd
            # Output : boolean
            if ticker in data_library.sell_signal_library : 
                df = data_library.sell_signal_library[ticker]
            else : 
                df = data_library.stock_price_library[ticker]
                df['sma_50'] = df['close'].rolling(50).mean()
                df['sma_5'] =  df['close'].rolling(5).mean()
                df['condition_1'] = df['close'] > df['sma_50'] * 1.5
                df['condition_2'] = df['sma_5'] < df['sma_50']
                df['sell_signal'] = df['condition_1'] | df['condition_2']
                data_library.add_stock_to_sell_signal_library(ticker, df)
            return df.loc[df.date_time == date_time]['sell_signal'].values[0]

        self.portfolio.monitor_sell_cond(sell_cond_func=sell_condition, sell_cond_params={
            'date_time' : '2021-05-26',
            'data_library' : self.data_library
        })
        self.assertEqual([], self.portfolio.positions_pending_to_sell)
        self.assertEqual(['2382'], list(self.data_library.sell_signal_library.keys()))
        self.portfolio.monitor_sell_cond(sell_cond_func=sell_condition, sell_cond_params={
            'date_time' : '2021-05-25',
            'data_library' : self.data_library
        })
        
        self.assertEqual(['2382'], self.portfolio.positions_pending_to_sell)
        

    # def test_boolean(self):
    #     a = True
    #     b = False
    #     self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()