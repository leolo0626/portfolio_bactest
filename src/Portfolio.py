from .Account import Account
from .Order import Order 

class Portfolio(Account) :
    def __init__ (self):
        super().__init__()
        self.size = 0
        self.positions = {}
    
    def add_long_position(self, order: Order):
        if order.action == 'b' and self.cash >= order.total_amount:
            self.positions[order.ticker] = {
                'ticker' : order.ticker,
                'price' : order.executed_price,
                'shares' : order.shares,
                'total_cost' : order.total_amount,
                'last_price' : None, 
                'market_value' : None, 
                'unrealized_pnl' : None, 
                'realized_pnl' : None
            }
            self.size = self.size + 1
            super().decrease_account_value(order.total_amount)
        else:
            raise Exception("Something went wrong in adding long position")
    
    def cover_position(self, order: Order):
        if order.ticker in self.positions and order.action == 's': 
            target_position = self.positions[order.ticker]
            if order.shares <= target_position['shares'] : 
                remaining_shares = target_position['shares'] - order.shares
                if remaining_shares == 0 : 
                    # Sold all position
                    target_position['shares'] = remaining_shares
                    target_position['realized_pnl'] = order.total_amount - target_position['total_cost']
                    super().increase_account_value(order.total_amount)
                    del self.positions[order.ticker]
                else :
                    pass

            else:
                raise Exception("Something went wrong in cover position : shares in cover order > shares in portfolio")
            self.size = self.size - 1
            return target_position
        else:
            raise Exception("Something went wrong in cover position ")




    
    





