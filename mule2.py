import myconfig
import socket
from dal_api import EquityDAO
from operator import attrgetter

mule_password = myconfig.mule_password
mule_network = myconfig.mule_network
mule_port = myconfig.mule_port

equityDAO = EquityDAO('localhost', 5000)


class IRC():
    def __init__(self, network, port, password, name):
        self.network = network
        self.port = port
        self.password = password
        self.name = name
        self.irc_socket = None

    def connect(self):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.settimeout(None)
        self.irc_socket.connect((self.network, self.port))

        self.send('PASS {}\n'.format(self.password))
        self.send('NICK {}\n'.format(self.name))
        self.send('USER {} {} {}:Python IRC\n'.format(self.name, self.name, self.name))
        self.send('JOIN #pynerds\n')
        self.send('PRIVMSG #pynerds :Here to serve you\n')

    def send(self, message):
        self.irc_socket.send(message.encode('utf-8'))

    def recv(self, bytes):
        return self.irc_socket.recv(bytes).decode('utf-8')

    def find(self, string_to_find):
        return self.irc_socket.find(string_to_find.encode('utf-8'))


def strip(string_to_strip):
    return string_to_strip.strip('\'').strip('\n').strip('\r')

irc = IRC(mule_network, mule_port, mule_password, 'mule2')
irc.connect()
keep_running = True
while keep_running:
    data = irc.recv ( 1024 )
    print(data)
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split() [ 1 ] + '\r\n')
    elif data.find('@mule2 help') != -1:
        irc.send('PRIVMSG #pynerds :I respond to stock <ticker>, dod, dow, div, drop, vol, tracked, meta, silent, vocal, and quit.\r\n')
    elif data.find('@mule2 quit') != -1:
        irc.send('PRIVMSG #pynerds :Ok bye.\r\n')
        irc.send('QUIT\r\n')
        keep_running = False
    elif data.find('@mule2 stock') != -1:
        tickers= data.split()
        ticker = strip(tickers[5]).upper()
        print('ticker = {}'.format(strip(tickers[5])))
        if ticker is None:
            irc.send('PRIVMSG #pynerds :Ticker not found.\r\n')
        else:
            equity = equityDAO.get_equity_with_most_recent_data(ticker, 5, 1)
            if equity is None:
                irc.send('PRIVMSG #pynerds :I couldn\'t find {}\r\n'.format(ticker))
            else:
                irc.send('PRIVMSG #pynerds :Found ticker {}\r\n'.format(ticker))
                #for s in equity.snapshots:
                #    if s.dividend_yield is None:
                #        s.dividend_yield = 0
                #    irc.send('PRIVMSG #pynerds : {}; {} ({:.2f}%)...dividend (yield): {}({:.2f})...P/E {}\r\n'.format(s.price, s.price_change, s.price_change_percent, s.dividend, s.dividend_yield, s.pe))

                #for ea in equity.aggregates:
                #    irc.send('PRIVMSG #pynerds : fifty day moving avg: {0}; fifty day volatility avg: {1}; % off recent high: {2}; % off recent low: {3}\r\n'.format(ea.fifty_day_moving_avg,
                #            ea.fifty_day_volatility_avg, ea.per_off_recent_high, ea.per_off_recent_low))
