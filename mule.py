import socket
from dal import EquityDAO

network = 'www.orangeshovel.com'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )

irc.send('NICK data_mule\r\n')
irc.send('USER data_mule data_mule data_mule :Python IRC\r\n')
irc.send('JOIN #pynerds\r\n' )
irc.send('PRIVMSG #pynerds :Here to serve you\r\n')
keep_running = True
while keep_running:
   data = irc.recv ( 1024 )
   if data.find('@mule help') != -1:
      irc.send('PRIVMSG #pynerds :I respond to stock <ticker> and quit.\r\n')
   if data.find('@mule quit') != -1:
      irc.send('PRIVMSG #pynerds :Ok bye.\r\n')
      irc.send('QUIT\r\n')
      keep_running = False
   if data.find('@mule stock') != -1:
      tickers= data.split()
      # example string as it comes from IRC:
      # :randall!u0076235@73.80.192.10 PRIVMSG #pynders :@botty sotck IBM
      ticker = tickers[5] 
      if ticker is None:
        irc.send('PRIVMSG #pynerds :Ticker not found.\r\n')
      else:
        equity = EquityDAO.get_equity_with_most_recent_data(ticker, 5, 1)
        if equity is None:
            irc.send('PRIVMSG #pynerds :You imbecile! I couldn\'t find {}\r\n'.format(ticker))
        else:
            irc.send('PRIVMSG #pynerds :{}\r\n'.format(ticker))
            for s in equity.snapshots:
                irc.send('PRIVMSG #pynerds : {0}; {1} ({2}%); dividend (yield): {3}({4}); P/E {5}\r\n'.format(s.price, s.price_change, s.price_change_percent, s.dividend, s.dividend_yield, s.pe))

#            for ea in equity.aggregates:
#                irc.send('PRIVMSG #pynerds : fifty day moving avg: {}; fifty day volatility avg: {}; % off recent high: {}; % off recent low: {}\r\n'.format(ea.fifty_day_moving_avg, \
#                         ea.fifty_day_volatility_avg, ea.per_off_recent_high, ea.per_off_recent_low))
