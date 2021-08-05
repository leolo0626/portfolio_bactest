from .Trade import Trade
class TradeRecordManager : 
    def __init__(self):
        self.trade_records = []
    
    def add_trade_record(self, trade : Trade):
        self.trade_records.append(trade)
