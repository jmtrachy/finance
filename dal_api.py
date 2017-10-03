from http_util import HTTPRequest
import myconfig


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


class EquityAggregate():
    def __init__(self, aggregate_id, equity_id, date, fifty_day_moving_avg, fifty_day_volatility_avg, per_off_recent_high, per_off_recent_low):
        self.aggregate_id = aggregate_id
        self.equity_id = equity_id
        self.date = date
        self.fifty_day_moving_avg = fifty_day_moving_avg
        self.fifty_day_volatility_avg = fifty_day_volatility_avg
        self.per_off_recent_high = per_off_recent_high
        self.per_off_recent_low = per_off_recent_low
        self.ticker = None

    def set_ticker(self, ticker):
        self.ticker = ticker


class EquityDAO():

    def __init__(self, api_host, api_port):
        self.host = api_host
        self.port = api_port

    def get_equity_with_most_recent_data(self, ticker, num_snapshots=5, num_aggregates=5):
        equity = self.get_equity_by_ticker(ticker)

        #if len(equities) > 0:
        #    equity = equities[0]
        #    equity.snapshots = EquityDAO.get_equity_snapshots_by_ticker(ticker, num_snapshots)
        #    equity.aggregates = EquityDAO.get_equity_aggregates_by_ticker(ticker, num_aggregates)

        return equity

    def convert_json_to_model(self, equity_json):
        equity = None

        if equity_json is not None:
            equity_id = equity_json.get('id')
            ticker = equity_json.get('ticker')
            name = equity_json.get('name')
            exchange = equity_json.get('exchange')
            industry = equity_json.get('industry')
            dow = equity_json.get('dow')

            equity = Equity(equity_id, ticker, name, exchange, industry, dow)

        return equity

    def get_equity_by_ticker(self, ticker):
        req = HTTPRequest(self.host, self.port, '/v1/equities/{}'.format(ticker))
        equity_json = req.send_request()

        equity = self.convert_json_to_model(equity_json)

        return equity
