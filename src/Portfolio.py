from .Account import Account
from .Order import Order 
from .Trade import Trade
from .DataLibrary import DataLibrary
from .TradeRecordManager import TradeRecordManager
from .AccountSummary import AccountSummary
from .ErrorManager import ErrorManager
from multiprocessing.pool import ThreadPool
import copy

class Portfolio(Account) :
    def __init__ (self, trade_record_manager : TradeRecordManager, account_summary : AccountSummary, error_manager : ErrorManager):
        super().__init__()
        self.size = 0
        self.positions = {}
        self.positions_pending_to_sell = []
        self.trade_record_manager = trade_record_manager
        self.account_summary = account_summary
        self.error_manager = error_manager

    
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

    def update_account_summary(self, date_time , data_library : DataLibrary, location='US') :
        positions = self.positions
        portfolio_threading = Portfolio_Multithread(position_dict=positions, date_time=date_time, data_library=data_library,
                                                    error_manager=self.error_manager)
        net_asset_value = portfolio_threading.run(positions)

        self.net_asset_value = net_asset_value + self.cash
        self.account_summary.add_account_summary(date_time, self.net_asset_value, self.cash)
        self.account_summary.add_position_history(date_time, copy.deepcopy(portfolio_threading.positions))
        self.positions = portfolio_threading.positions



    def monitor_sell_cond(self, sell_cond_func, sell_cond_params):
        for position in self.positions : 
            sell_cond_params['ticker'] = position
            if sell_cond_func(**sell_cond_params) :
                self.positions_pending_to_sell.append(self.positions[position])






    
    
class Portfolio_Multithread :
    def __init__(self, position_dict, date_time, data_library, error_manager):
        self.positions = position_dict
        self.date_time = date_time
        self.data_library = data_library
        self.error_manager = error_manager

    def update_position_value(self, position, location='US'):

        stock_price = self.data_library.read_csv(position, location)
        try:
            closing_price = stock_price.loc[stock_price.date_time == self.date_time, 'close'].values[0]
        except:
            error_message = f"{position} does not have last price at {self.date_time}"
            # print(error_message)
            closing_price = self.positions[position]['last_price']
            if closing_price is None:
                closing_price = self.positions[position]['price']
            self.error_manager.add_error_message(position, "update_account_summary", error_message)

        self.positions[position]['last_price'] = closing_price
        self.positions[position]['market_value'] = closing_price * self.positions[position]['shares']
        self.positions[position]['unrealized_pnl'] = self.positions[position]['market_value'] - self.positions[position]['total_cost']
        return self.positions[position]['market_value']

    def run(self, positions):
        t = ThreadPool(processes=8)
        market_cap_value_list = t.map(self.update_position_value, list(positions.keys()))
        t.close()
        return sum(market_cap_value_list)


