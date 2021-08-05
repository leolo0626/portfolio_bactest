from .Account import Account
from .Order import Order 
from .Trade import Trade
from .DataLibrary import DataLibrary
from .TradeRecordManager import TradeRecordManager
from .AccountSummary import AccountSummary

class Portfolio(Account) :
    def __init__ (self, trade_record_manager : TradeRecordManager, account_summary : AccountSummary):
        super().__init__()
        self.size = 0
        self.positions = {}
        self.positions_pending_to_sell = []
        self.trade_record_manager = trade_record_manager
        self.account_summary = account_summary

    
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
            self.trade_record_manager.add_trade_record(Trade(order))
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
            self.trade_record_manager.add_trade_record(Trade(order))
            return target_position
        else:
            raise Exception("Something went wrong in cover position ")

    def update_account_summary(self, date_time , data_library : DataLibrary) :
        net_asset_value = 0
        for position in self.positions : 
            stock_price = data_library.stock_price_library[position]
            closing_price = stock_price.loc[stock_price.date_time == date_time, 'close'].values[0]
            self.positions[position]['last_price'] = closing_price
            self.positions[position]['market_value'] = closing_price * self.positions[position]['shares']
            self.positions[position]['unrealized_pnl'] = self.positions[position]['market_value'] - self.positions[position]['total_cost']
            net_asset_value = net_asset_value + self.positions[position]['market_value'] 
        self.net_asset_value = net_asset_value + self.cash
        self.account_summary.add_account_summary(date_time, self.net_asset_value, self.cash)
        self.account_summary.add_position_history(date_time, self.positions)


    def monitor_sell_cond(self, sell_cond_func, sell_cond_params):
        for position in self.positions : 
            sell_cond_params['ticker'] = position
            if sell_cond_func(**sell_cond_params) :
                self.positions_pending_to_sell.append(self.positions[position])






    
    





