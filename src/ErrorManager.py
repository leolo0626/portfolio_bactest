class ErrorManager :
    def __init__(self):
        self.error_collection = []

    def add_error_message(self, ticker, error_func, error_message):
        self.error_collection.append({
            'ticker' : ticker,
            'error_func' : error_func,
            'error_message' : error_message
        })