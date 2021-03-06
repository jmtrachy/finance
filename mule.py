import myconfig
import socket
from dal import EquityDAO
from operator import attrgetter

password = myconfig.mule_password
network = myconfig.mule_network
port = myconfig.mule_port
all_equities = set()
silenced = False

def build_ticker_set():
   all_equities_raw = sorted(EquityDAO.get_equities(), key=attrgetter('ticker'), reverse=False)
   for e in all_equities_raw:
      all_equities.add(e.ticker)

def get_recent_snapshots(equities):
   recent_snapshots = []
   for equity in equities:
      recent_snapshot = EquityDAO.get_most_recent_snapshots([equity])
      for e in recent_snapshot:
         recent_snapshots.append(e)

   return recent_snapshots

def get_recent_aggregates(equities):
   aggregates = []
   for equity in equities:
      aggregates.append(EquityDAO.get_recent_aggregate(equity)[0])

   return aggregates 

build_ticker_set()
print('mule is connecting to ' + str(network) + ':' + str(port))
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM )
irc.settimeout(None)
irc.connect((network, port))

irc.send('PASS ' + password + '\r\n')
irc.send('NICK mule\r\n')
irc.send('USER mule mule mule :Python IRC\r\n')
irc.send('JOIN #pynerds\r\n' )
irc.send('PRIVMSG #pynerds :Here to serve you\r\n')
keep_running = True
while keep_running:
   data = irc.recv ( 1024 )
   if data.find('PING') != -1:
      irc.send('PONG ' + data.split() [ 1 ] + '\r\n')
   elif data.find('@mule help') != -1:
      irc.send('PRIVMSG #pynerds :I respond to stock <ticker>, dod, dow, div, drop, vol, tracked, meta, silent, vocal, and quit.\r\n')
   elif data.find('@mule quit') != -1:
      irc.send('PRIVMSG #pynerds :Ok bye.\r\n')
      irc.send('QUIT\r\n')
      keep_running = False
   elif data.find('@mule stock') != -1:
      tickers= data.split()
      ticker = tickers[5].upper()
      if ticker is None:
        irc.send('PRIVMSG #pynerds :Ticker not found.\r\n')
      else:
        equity = EquityDAO.get_equity_with_most_recent_data(ticker, 5, 1)
        if equity is None:
            irc.send('PRIVMSG #pynerds :I couldn\'t find {}\r\n'.format(ticker))
        else:
            irc.send('PRIVMSG #pynerds :{}\r\n'.format(ticker))
            for s in equity.snapshots:
                if s.dividend_yield is None:
                    s.dividend_yield = 0 
                irc.send('PRIVMSG #pynerds : {}; {} ({:.2f}%)...dividend (yield): {}({:.2f})...P/E {}\r\n'.format(s.price, s.price_change, s.price_change_percent, s.dividend, s.dividend_yield, s.pe))

            for ea in equity.aggregates:
                irc.send('PRIVMSG #pynerds : fifty day moving avg: {0}; fifty day volatility avg: {1}; % off recent high: {2}; % off recent low: {3}\r\n'.format(ea.fifty_day_moving_avg, \
                         ea.fifty_day_volatility_avg, ea.per_off_recent_high, ea.per_off_recent_low))
   elif data.find('@mule dod') != -1:
      recent_snapshots = get_recent_snapshots(EquityDAO.get_dow_equities())
      equities = sorted(recent_snapshots, key=attrgetter('dividend_yield'), reverse=True)
     
      irc.send('PRIVMSG #pynerds :Dogs of the DOW\r\n')
      
      for j in range(0, 10):
         stock = equities[j]
         equity = EquityDAO.get_equity_by_id(stock.equity_id)
         irc.send('PRIVMSG #pynerds :{}. {} yields {:.2f}%\r\n'.format(j + 1, equity.ticker, stock.dividend_yield))

   elif data.find('@mule dow') != -1:
      recent_snapshots = get_recent_snapshots(EquityDAO.get_dow_equities())
      recent_snapshots = sorted(recent_snapshots, key=attrgetter('price_change'), reverse=True)

      j = 1
      for snapshot in recent_snapshots:
         equity = EquityDAO.get_equity_by_id(snapshot.equity_id)
         irc.send('PRIVMSG #pynerds :{}. {} is at {}.  {:.2f}% from yesterday\r\n'.format(j, equity.ticker, snapshot.price, snapshot.price_change))
         j += 1

   elif data.find('@mule div') != -1:
      recent_snapshots = get_recent_snapshots(EquityDAO.get_equities())
      equities = sorted(recent_snapshots, key=attrgetter('dividend_yield'), reverse=True)
     
      irc.send('PRIVMSG #pynerds :Top tracked dividend stocks\r\n')

      if len(equities) > 0:
      
         for j in range(0, 10):
            stock = equities[j]
            equity = EquityDAO.get_equity_by_id(stock.equity_id)
            irc.send('PRIVMSG #pynerds :{}. {} yields {:.2f}%\r\n'.format(j + 1, equity.ticker, stock.dividend_yield))

   elif data.find('@mule drop') != -1:
      recent_aggregates = get_recent_aggregates(EquityDAO.get_equities())
      aggregates = sorted(recent_aggregates, key=attrgetter('per_off_recent_high'), reverse=True)

      irc.send('PRIVMSG #pynerds :Biggers recent losers\r\n')

      for j in range(0, 10):
         aggregate = aggregates[j]
         equity = EquityDAO.get_equity_by_id(aggregate.equity_id)
         irc.send('PRIVMSG #pynerds :{}. {} is off {:.2f}% from its recent high\r\n'.format(j + 1, equity.ticker, aggregate.per_off_recent_high))

   elif data.find('@mule vol') != -1:
      recent_aggregates = get_recent_aggregates(EquityDAO.get_equities())
      aggregates = sorted(recent_aggregates, key=attrgetter('fifty_day_volatility_avg'), reverse=True)

      irc.send('PRIVMSG #pynerds :Most volatile stocks recently\r\n')

      for j in range(0, 10):
         aggregate = aggregates[j]
         equity = EquityDAO.get_equity_by_id(aggregate.equity_id)
         irc.send('PRIVMSG #pynerds :{}. {} on average moves {:.2f}% per day\r\n'.format(j + 1, equity.ticker, aggregate.fifty_day_volatility_avg))

   elif data.find('@mule tracked') != -1:
      equities = sorted(EquityDAO.get_equities(), key=attrgetter('ticker'), reverse=False)

      irc.send('PRIVMSG #pynerds :All currently tracked stocks\r\n')

      equity_list = ''
      for equity in equities:
         equity_list += ', ' + equity.ticker

      equity_list = equity_list[2:]
      irc.send('PRIVMSG #pynerds :{}\r\n'.format(equity_list)) 
   
   elif data.find('@mule meta') != -1:
      equities = EquityDAO.get_equity_meta()

      irc.send('PRIVMSG #pynerds :Meta on all currently traded stocks.  Format: ticker (number of days tracked)\r\n')

      equity_list = ''
      for equity in equities:
         equity_list += ', ' + equity.ticker + ' (' + str(equity.num_days_tracked) + ')'

      equity_list = equity_list[2:]
      irc.send('PRIVMSG #pynerds :{}\r\n'.format(equity_list)) 
   elif data.find('@mule silent') != -1:
      silenced = True
      irc.send('PRIVMSG #pynerds :Ok I\'ll try to be a fly on the wall.\r\n')
   elif data.find('@mule vocal') != -1:
      silenced = False
      irc.send('PRIVMSG #pynerds :Gag order rescinded.\r\n')
   elif not silenced:
      if data is not None and data != '':
         all_words = data.split(' ')
         count = 0
         for word in all_words:
            if count > 2:
               word_stripped = word.strip(':').strip(',').strip('.').strip('\n').strip('\r').upper()
               if word_stripped in all_equities:
                  equity = EquityDAO.get_equity_with_most_recent_data(word_stripped, 1, 1)
                  irc.send('PRIVMSG #pynerds :{} last closed at {}\r\n'.format(equity.ticker, equity.snapshots[0].price))
            count += 1
