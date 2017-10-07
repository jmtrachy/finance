import myconfig
import bot
from dal_api import EquityDAO

mule_password = myconfig.mule_password
mule_network = myconfig.mule_network
mule_port = myconfig.mule_port

equityDAO = EquityDAO('localhost', 5000)

def get_stock_info(arguments):
    if arguments is None:
        return None
    ticker = arguments.strip(' ').upper()
    print('ticker = {}'.format(ticker))
    messages = []

    if ticker is None:
        messages.append('No ticker provided.')
    else:
        equity = equityDAO.get_equity_with_most_recent_data(ticker, 5, 1)
        if equity.ticker is None:
            messages.append('I couldn\'t find {}'.format(ticker))
        else:
            messages.append('Found ticker {}'.format(ticker))
            for s in equity.snapshots:
                if s.dividend_yield is None:
                    s.dividend_yield = 0
                messages.append(' {}; {} {}%)...dividend (yield): {}({})...P/E {}'.format(s.price,
                                                                                          s.price_change,
                                                                                          s.price_change_percent,
                                                                                          s.dividend,
                                                                                          s.dividend_yield,
                                                                                          s.pe))

            for ea in equity.aggregates:
                messages.append(
                    ' fifty day moving avg: {0}; fifty day volatility avg: {1}; % off recent high: {2}; % off recent low: {3}'.format(
                        ea.fifty_day_moving_avg,
                        ea.fifty_day_volatility_avg, ea.per_off_recent_high, ea.per_off_recent_low))
    return messages

def get_tracked_stocks(arguments):
    equities = equityDAO.get_all_equities()
    list_of_equities = ''

    for equity in equities:
        list_of_equities += '{},'.format(equity.ticker)

    return list_of_equities.strip(',')


if __name__ == '__main__':
    bot = bot.Bot('mule2', 'Better than the first')

    bot.add_complex_listener('stock', get_stock_info)
    bot.add_simple_listener('tracked', get_tracked_stocks)

    bot.connect(mule_network, mule_port, 'pynerds', mule_password)
