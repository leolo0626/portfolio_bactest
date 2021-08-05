class AccountSummary :
    def __init__(self):
        self.history = []
        self.position_history = {}
    
    def add_account_summary(self, date_time,  nav, cash) :
        self.history.append({'date_time' : date_time, 'nav': nav, 'cash' : cash})

    def add_position_history(self, date_time, positions):
        self.position_history[date_time] = positions