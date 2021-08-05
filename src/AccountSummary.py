class AccountSummary :
    def __init__(self):
        self.history = []
    
    def add_account_summary(self, date_time,  nav, cash) :
        self.history.append({'date_time' : date_time, 'nav': nav, 'cash' : cash})