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

    @staticmethod
    def convert_equity_json_to_model(equity_json):
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

    @staticmethod
    def convert_snapshot_json_to_model(snapshot_json):

        if snapshot_json is not None:
            snapshot_id = snapshot_json.get('id')
            equity_id = snapshot_json.get('equityId')
            date = snapshot_json.get('date')
            price = snapshot_json.get('price')
            price_change = snapshot_json.get('priceChange')
            price_change_percent = snapshot_json.get('priceChangePercent')
            dividend = snapshot_json.get('dividend')
            dividend_yield = snapshot_json.get('dividendYield')
            pe = snapshot_json.get('pe')

            snapshot = EquitySnapshot(snapshot_id, equity_id, date, price, price_change, price_change_percent,
                                      dividend, dividend_yield, pe)
        return snapshot

    @staticmethod
    def convert_aggregate_json_to_model(aggregate_json):
        aggregate = None

        if aggregate_json is not None:
            aggregate_id = aggregate_json.get('id')
            equity_id = aggregate_json.get('equityId')
            date = aggregate_json.get('date')
            fifty_day_moving_avg = aggregate_json.get('fiftyDayMovingAverage')
            fifty_day_volatility_avg = aggregate_json.get('fiftyDayVolatilityAverage')
            per_off_recent_high = aggregate_json.get('perOffRecentHigh')
            per_off_recent_low = aggregate_json.get('perOffRecentLow')

            aggregate = EquityAggregate(aggregate_id, equity_id, date, fifty_day_moving_avg, fifty_day_volatility_avg,
                                        per_off_recent_high, per_off_recent_low)
        return aggregate

    # Gets the base equity information along with the n daily snapshots and the last n daily aggregates
    def get_equity_with_most_recent_data(self, ticker, num_snapshots=5, num_aggregates=1):
        equity = self.get_equity_by_ticker(ticker)

        if equity is not None:
            equity.snapshots = self.get_equity_snapshots_by_ticker(ticker, num_snapshots)
            equity.aggregates = self.get_equity_aggregates_by_ticker(ticker, num_aggregates)

        return equity

    # Returns all stocks that are part of the DOW
    def get_dow_equities(self):
        req = HTTPRequest(self.host, self.port, '/v1/equities?filter=dow')
        result_json = req.send_request()

        equities = []
        for e in result_json:
            equity = self.convert_equity_json_to_model(e)
            equities.append(equity)

        return equities

    # Retrieves n daily equity snapshots based on the desired ticker symbol
    def get_equity_snapshots_by_ticker(self, ticker, num_snapshots=5):
        req = HTTPRequest(self.host, self.port, '/v1/equities/{}/snapshots?limit={}'.format(ticker, num_snapshots))
        result_json = req.send_request()

        snapshots = []
        for s in result_json:
            snapshot = self.convert_snapshot_json_to_model(s)
            snapshots.append(snapshot)

        return snapshots

    # Retrieves the actual ticker information
    def get_equity_by_ticker(self, ticker):
        req = HTTPRequest(self.host, self.port, '/v1/equities/{}'.format(ticker))
        equity_json = req.send_request()

        equity = self.convert_equity_json_to_model(equity_json)

        return equity

    # Retrieves the last n daily aggregates for an individual ticker
    def get_equity_aggregates_by_ticker(self, ticker, num_aggregates):
        req = HTTPRequest(self.host, self.port, '/v1/equities/{}/aggregates?limit={}'.format(ticker, num_aggregates))
        result_json = req.send_request()

        aggregates = []
        for a in result_json:
            aggregate = self.convert_aggregate_json_to_model(a)
            aggregates.append(aggregate)

        return aggregates

    # Retrieves all equities tracked by the system
    def get_all_equities(self):
        req = HTTPRequest(self.host, self.port, '/v1/equities/')
        result_json = req.send_request()

        equities = []
        for e in result_json:
            equity = self.convert_equity_json_to_model(e)
            equities.append(equity)

        return equities