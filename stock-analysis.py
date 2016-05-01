class Analyzer():
    def __init__(self, equities):
        self.equities = equities
        self.summaries = {}
        self.breakout_equities()

    def breakout_equities(self):
        for equity in self.equities:
            if equity.ticker not in self.summaries:
                summary = Summary(equity.ticker, equity.name, equity.exchange)
                self.summaries[equity.ticker] = summary
            else:
                summary = self.summaries[equity.ticker]

            summary.add_price_point(PricePoint(equity.price, equity.date))

    def analyze(self):
        for summary_name in self.summaries:
            summary = self.summaries[summary_name]

            min_price = None
            max_price = None
            two_hundred_date_average = 0
            num_price_points = 0
            current_price = None
            recent_high = 0.0

            for price_point in summary.price_points:

                if num_price_points == 0:
                    current_price = price_point.price

                if min_price is None:
                    min_price = price_point.price
                elif min_price > price_point.price:
                    min_price = price_point.price

                if max_price is None:
                    max_price = price_point.price
                elif max_price < price_point.price:
                    max_price = price_point.price

                if num_price_points < 200:
                    two_hundred_date_average += price_point.price

                if recent_high < price_point.price and num_price_points < 100:
                    recent_high = price_point.price

                num_price_points += 1

            summary.two_hundred_day_avg = two_hundred_date_average / num_price_points
            summary.min_price = min_price
            summary.max_price = max_price
            summary.per_off_recent_high = 1 - current_price / recent_high

            print(summary.ticker + ' current price = ' + str(current_price))
            print(summary.ticker + ' min price = ' + str(summary.min_price))
            print(summary.ticker + ' max price = ' + str(summary.max_price))
            print(summary.ticker + ' 200 day avg = ' + str(summary.two_hundred_day_avg))
            print(summary.ticker + ' % down from recent high = {:.2%}'.format(summary.per_off_recent_high) + '%')


class PricePoint():
    def __init__(self, price, date):
        self.price = price
        self.date = date


class Summary():
    def __init__(self, ticker, name, exchange):
        self.ticker = ticker
        self.exchange = exchange
        self.name = name
        self.price_points = []

    def add_price_point(self, price_point):
        self.price_points.append(price_point)


class Equity():
    def __init__(self, snapshot_id, ticker, name, exchange, date, price):
        self.snapshot_id = snapshot_id
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.date = date
        self.price = price


if __name__ == "__main__":
    equities_to_analyze = []
    equities_to_analyze.append(Equity(1, 'SCTY', 'Solar City', 'NASDAQ', '2016-04-29', 30.79))
    equities_to_analyze.append(Equity(1, 'SCTY', 'Solar City', 'NASDAQ', '2016-04-28', 33.73))
    equities_to_analyze.append(Equity(1, 'SCTY', 'Solar City', 'NASDAQ', '2016-04-27', 33.70))
    equities_to_analyze.append(Equity(1, 'SCTY', 'Solar City', 'NASDAQ', '2016-04-26', 33.46))

    equities_to_analyze.append(Equity(1, 'TOT', 'Total', 'NYSE', '2016-04-29', 50.65))
    equities_to_analyze.append(Equity(1, 'TOT', 'Total', 'NYSE', '2016-04-28', 51.01))
    equities_to_analyze.append(Equity(1, 'TOT', 'Total', 'NYSE', '2016-04-27', 51.14))
    equities_to_analyze.append(Equity(1, 'TOT', 'Total', 'NYSE', '2016-04-26', 49.77))

    analyzer = Analyzer(equities_to_analyze)
    analyzer.analyze()
