class Order : 
    def __init__(self, ticker, date_time , executed_price, shares, commission=0, action='b'):
        self.ticker = ticker
        self.date_time = date_time
        self.executed_price = executed_price
        self.shares = shares
        self.commission = commission
        self.action = action
        if action == 'b' : 
            self.total_amount = executed_price * shares + commission
        elif action == 's': 
            self.total_amount = executed_price * shares - commission

    
