import httplib
import MySQLdb
import datetime
import time
import random
from xml.dom.minidom import parse, parseString

class ScreenScraper():
    def __init__(self, equities):
        self.equities = equities

    def run(self):
        for equity in self.equities:
            screen_scrape = self.request_equity(equity)
            self.parse_equity(equity, screen_scrape)
            self.persist_equity(equity)
            time.sleep(random.randint(1, 10))

    def request_equity(self, equity):
        h1 = httplib.HTTPSConnection('www.google.com')
        equity_url = '/finance?q=' + equity.exchange + '%3A' + equity.ticker
        h1.request("GET", equity_url)

        response = h1.getresponse()
        return response.read()

    def parse_equity(self, equity, screen_scrape):
        div_index = screen_scrape.index('<div id="sharebox-data"')
        temp_string = screen_scrape[div_index:]

        div_close_index = temp_string.index('</div>')
        xml_snippet = temp_string[:div_close_index + 6]
        containing_div = xml_snippet.index('">')

        xml_snippet = xml_snippet[:containing_div + 1] + ' ' + xml_snippet[containing_div + 1:]
        xml_snippet = xml_snippet.replace('&', '&amp;')
        xml_snippet = xml_snippet.replace('">', '"/>')

        dom = parseString(xml_snippet)
        children = dom.getElementsByTagName('meta')

        for child in children:
            field_name = child.attributes['itemprop'].value
            field_value = child.attributes['content'].value
            if field_name == 'price':
                print(equity.ticker + ' = ' + field_value)
                equity.price = field_value
            elif field_name == 'name':
                equity.name = field_value
            elif field_name == 'quoteTime':
                equity.quote_time = field_value

    def persist_equity(self, equity):
        cnx = None
        cursor = None
        try:
            # prepared statement for adding an equity snapshot
            insert_equity_snapshot = ('INSERT INTO `equity_snapshot` (`ticker`, `name`, `exchange`, `date`, `price`) VALUES (%s, %s, %s, %s, %s)')

            cnx = MySQLdb.connect(host='localhost', # your host, usually localhost
                     user='jimbob', # your username
                     passwd='finance', # your password
                     db='finance') # name of the data base
            # always do this to set mysqldb to use utf-8 encoding rather than latin-1
            cnx.set_character_set('utf8')
            cursor = cnx.cursor()
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')
          
            date_str = equity.quote_time[:10]
            data_equity = equity.ticker, equity.name, equity.exchange, date_str, equity.price
            print('Inserting ' + equity.ticker)
            cursor.execute(insert_equity_snapshot, data_equity)
               
        finally:
            cnx.commit()
            cursor.close()
            cnx.close()
        

class Equity():
    def __init__(self, exchange, ticker):
        self.exchange = exchange
        self.ticker = ticker

if __name__ == "__main__":
    stocks = []

    # Energy
    stocks.append(Equity('NASDAQ', 'SCTY'))
    stocks.append(Equity('NYSE', 'TOT'))
    stocks.append(Equity('NYSE', 'XOM'))
    stocks.append(Equity('NYSE', 'CVX'))
    stocks.append(Equity('NYSE', 'PSX'))

    # Industrial
    stocks.append(Equity('NYSE', 'GE'))
    stocks.append(Equity('NYSE', 'MMM'))
    stocks.append(Equity('NYSE', 'CAT'))
    stocks.append(Equity('NYSE', 'DD'))

    # Technology 
    stocks.append(Equity('NASDAQ', 'AKAM'))
    stocks.append(Equity('NYSE', 'IBM'))
    stocks.append(Equity('NYSE', 'SAP'))
    stocks.append(Equity('NASDAQ', 'AAPL'))
    stocks.append(Equity('NASDAQ', 'CSCO'))
    stocks.append(Equity('NASDAQ', 'INTC'))
    stocks.append(Equity('NASDAQ', 'MSFT'))
    stocks.append(Equity('NYSE', 'UTX'))

    # Misc
    stocks.append(Equity('NYSE', 'SVU'))
    stocks.append(Equity('NYSE', 'DIS'))
    stocks.append(Equity('NYSE', 'BA'))
    stocks.append(Equity('NYSE', 'HD'))
    stocks.append(Equity('NYSE', 'KO'))
    stocks.append(Equity('NYSE', 'MCD'))
    stocks.append(Equity('NYSE', 'NKE'))
    stocks.append(Equity('NYSE', 'TRV'))
    stocks.append(Equity('NYSE', 'WMT'))

    # Automotive
    stocks.append(Equity('NASDAQ', 'TSLA'))
    stocks.append(Equity('ETR', 'VOW'))
    stocks.append(Equity('NYSE', 'F'))

    # Communications
    stocks.append(Equity('NYSE', 'T'))
    stocks.append(Equity('NYSE', 'VZ'))

    # Media
    stocks.append(Equity('NASDAQ', 'NFLX'))

    # Financial
    stocks.append(Equity('NYSE', 'JPM'))
    stocks.append(Equity('NYSE', 'WFC'))
    stocks.append(Equity('NYSE', 'GS'))
    stocks.append(Equity('NYSE', 'AXP'))
    stocks.append(Equity('NYSE', 'V'))

    # Pharma
    stocks.append(Equity('NYSE', 'PFE'))
    stocks.append(Equity('NYSE', 'MRK'))

    # Health
    stocks.append(Equity('NYSE', 'JNJ'))
    stocks.append(Equity('NYSE', 'UNH'))
    stocks.append(Equity('NYSE', 'PG'))

    ss = ScreenScraper(stocks)
    ss.run()
