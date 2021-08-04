class DataLibrary :
    def __init__(self):
        self.sell_signal_library = {}
        self.stock_price_library = {}
    
    def add_stock_to_sell_signal_library(self, ticker, sell_signal_data):
        self.sell_signal_library[ticker] = sell_signal_data
    
    def add_stock_price_library(self, ticker, stock_price_data):
        self.stock_price_library[ticker] = stock_price_data