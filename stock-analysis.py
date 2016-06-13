import MySQLdb
import notification
import dal

class Analyzer():
    def __init__(self, equities):
        self.equities = equities
        self.summaries = {}
        #self.industry_summaries = {}
        self.load_snapshots()

    def load_snapshots(self):
        for equity in self.equities:
            equity.snapshots = dal.EquityDAO.get_equity_snapshots_by_ticker(equity.ticker, 50)

    def analyze(self, debug_mode=False):
        for equity in self.equities:

            min_price = None
            max_price = None
            fifty_day_moving_sum = 0
            fifty_day_moving_avg = 0
            fifty_day_volatility_sum = 0
            fifty_day_volatility_avg = 0
            num_price_points = 0
            current_price = None
            recent_high = None
            recent_low = None

            for snapshot in equity.snapshots:

                current_price = snapshot.price

                if min_price is None:
                    min_price = current_price
                elif min_price > current_price:
                    min_price = current_price

                if max_price is None:
                    max_price = current_price
                elif max_price < current_price:
                    max_price = current_price

                if num_price_points < 50:
                    fifty_day_moving_sum += current_price
                    fifty_day_volatility_sum += abs(snapshot.price_change_percent)

                if recent_high is None:
                    recent_high = current_price
                if recent_low is None:
                    recent_low = current_price

                if num_price_points < 100:
                    if recent_high < current_price:
                        recent_high = current_price
                    if recent_low > current_price:
                        recent_low = current_price

                num_price_points += 1

            if num_price_points > 50:
                fifty_day_moving_avg = fifty_day_moving_sum / 50
                fifty_day_volatility_avg = fifty_day_volatility_sum / 50
            else:
                fifty_day_moving_avg = fifty_day_moving_sum / num_price_points
                fifty_day_volatility_avg = fifty_day_volatility_sum / num_price_points

            per_off_recent_high = 100 * (1 - current_price / recent_high)
            per_off_recent_low = 100 * (current_price / recent_low - 1)

            if debug_mode:
                print('equity.equity_id = ' + str(equity.equity_id))
                print('current price = ' + str(current_price))
                print('recent_high = ' + str(recent_high))
                print('recent_low = ' + str(recent_low))
                print('fifty_day_moving_avg = ' + str(fifty_day_moving_avg))
                print('fifty_day_volatility_avg = ' + str(fifty_day_volatility_avg))
                print('per_off_recent_high = ' + str(per_off_recent_high))
                print('per_off_recent_low = ' + str(per_off_recent_low))

            aggregate = dal.EquityAggregate(None, equity.equity_id, None, fifty_day_moving_avg, fifty_day_volatility_avg, per_off_recent_high, per_off_recent_low)
            dal.EquityDAO.create_equity_aggregate(aggregate)


if __name__ == "__main__":
    equities_to_analyze = dal.EquityDAO.get_equities()
#    equities_to_analyze = dal.EquityDAO.get_equity_by_ticker('SCTY')    
    analyzer = Analyzer(equities_to_analyze)
    analyzer.analyze()

    #notification.NotificationService.notify_irc(analyzer.summaries)
