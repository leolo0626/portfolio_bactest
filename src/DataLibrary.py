import pandas as pd
class DataLibrary :
    def __init__(self, path):
        self.path = path
        self.sell_signal_library = {}
        self.buy_signal_library = {}
        self.stock_price_library = {}
        
    def add_stock_to_sell_signal_library(self, ticker, sell_signal_data):
        self.sell_signal_library[ticker] = sell_signal_data
    
    def add_stock_to_buy_signal_library(self, ticker, buy_signal_data) :
        self.buy_signal_library[ticker] = buy_signal_data
    
    def add_stock_price_library(self, ticker, stock_price_data):
        self.stock_price_library[ticker] = stock_price_data

    def read_csv(self, ticker, location):
        return pd.read_csv(self.path + '/' + ticker + f'_{location}.csv')

    
    