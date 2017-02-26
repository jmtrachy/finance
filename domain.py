class Equity():
    def __init__(self, equity_id, ticker, name, exchange, industry, dow):
        self.equity_id = equity_id
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.industry = industry
        self.snapshots = []
        self.aggregates = []
        self.dow = dow


class EquitySnapshot():
    def __init__(self, snapshot_id, equity_id, date, price, price_change, price_change_percent, dividend=None, dividend_yield=None, pe=None):
        self.snapshot_id = snapshot_id
        self.equity_id = equity_id
        self.date = date
        self.price = price
        self.price_change = price_change
        self.price_change_percent = price_change_percent
        self.dividend = dividend
        self.dividend_yield = dividend_yield
        self.pe = pe