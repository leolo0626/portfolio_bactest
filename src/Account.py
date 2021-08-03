class Account :
    def __init__(self):
        self.initial_capital = 0
        self.cash = 0 
        self.net_asset_value = 0
    
    def add_capital(self, cash_amount):
        self.initial_capital = self.initial_capital + cash_amount
        self.cash = self.cash + cash_amount
        self.net_asset_value = self.net_asset_value + cash_amount
    
    def increase_account_value(self, amount):
        self.cash = self.cash + amount
        
    def decrease_account_value(self, amount):
        self.cash = self.cash - amount