__author__ = 'james trachy'

import argparse
import bot
from dal_api import EquityDAO
import myconfig
from operator import attrgetter

mule_password = myconfig.mule_password
mule_network = myconfig.mule_network
mule_port = myconfig.mule_port
mule_name = 'mule2'

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


def get_dow_stocks(arguments):
    equities = equityDAO.get_dow_equities()
    dow_snapshots = []

    for equity in equities:
        snapshots = equityDAO.get_equity_snapshots_by_ticker(equity.ticker, 1)
        if len(snapshots) > 0:
            s = snapshots[0]
            s.ticker = equity.ticker
            dow_snapshots.append(s)

    dow_snapshots = sorted(dow_snapshots, key=attrgetter('price_change_percent'), reverse=True)

    message = ''
    for s in dow_snapshots:
        message += '{} ==> {}\n'.format(s.ticker, s.price_change_percent)

    return message.strip('\n')


def get_div_stocks(arguments):
    equities = equityDAO.get_all_equities()
    div_snapshots = []

    for equity in equities:
        snapshots = equityDAO.get_equity_snapshots_by_ticker(equity.ticker, 1)
        if len(snapshots) > 0:
            s = snapshots[0]
            s.ticker = equity.ticker
            if s.dividend_yield is not None:
                div_snapshots.append(s)

    div_snapshots = sorted(div_snapshots, key=attrgetter('dividend_yield'), reverse=True)

    message = ''
    count = 1
    for s in div_snapshots:
        if count <= 10:
            message += '{} ==> {}\n'.format(s.ticker, s.dividend_yield)
            count += 1

    return message.strip('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gathering arguments')
    parser.add_argument('-t', '--test_mode', action='store_true', help='Do not connect to a server, just ask for commands')
    args = parser.parse_args()

    if args.test_mode:
        command = None
        while command != 'quit':
            raw_input = input('What is your command?')
            tokens = raw_input.split(' ')
            command = tokens[0]

            if command == 'stock':
                print(get_stock_info(tokens[1]))
            elif command == 'tracked':
                print(get_tracked_stocks(''))
            elif command == 'help':
                print('In test mode I support stock, tracked, help')
            elif command == 'dow':
                print(get_dow_stocks(None))
            elif command == 'div':
                print(get_div_stocks(None))

    else:
        bot = bot.Bot(mule_name, 'Better than the first')

        bot.add_complex_listener('stock', get_stock_info)
        bot.add_simple_listener('tracked', get_tracked_stocks)
        bot.add_simple_listener('dow', get_dow_stocks)
        bot.add_simple_listener('div', get_div_stocks)

        bot.connect(mule_network, mule_port, 'pynerds', mule_password)
