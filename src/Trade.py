from .Order import Order
class Trade :
    def __init__(self, order : Order):
        self.ticker = order.ticker
        self.trade_date = order.date_time
        self.order_action = order.action
        self.price = order.executed_price
        self.shares = order.shares
        self.commission = order.commission
        self.total_amount = order.total_amount

