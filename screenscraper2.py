import dal
import httplib
import MySQLdb
import datetime
import time
import random
from xml.dom.minidom import parse, parseString
from argparse import ArgumentParser
from dal import EquityDAO

class ScreenScraper():
    def run(self):
        equities_to_scrape = EquityDAO.get_equities()

        for equity in equities_to_scrape:
            screen_scrape = self.request_equity(equity)
            equity_snapshot = self.parse_equity(equity, screen_scrape)
            self.persist_equity_snapshot(equity_snapshot)
            time.sleep(random.randint(1, 10))

    def request_equity(self, equity):
        h1 = httplib.HTTPSConnection('www.google.com')
        equity_url = '/finance?q=' + equity.exchange + '%3A' + equity.ticker
        h1.request("GET", equity_url)

        response = h1.getresponse()
        return response.read()

    def parse_equity(self, equity, screen_scrape, print_data=False):
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
            if print_data:
                print(field_name + ' = ' + field_value)
            if field_name == 'price':
                price = field_value
            elif field_name == 'name':
                name = field_value
            elif field_name == 'quoteTime':
                quote_time = field_value[:10]
            elif field_name == 'priceChange':
                price_change = field_value
            elif field_name == 'priceChangePercent':
                price_change_percent = field_value

        return dal.EquitySnapshot(None, equity.equity_id, quote_time, price, price_change, price_change_percent)

    def persist_equity_snapshot(self, equity_snapshot):
        EquityDAO.create_equity_snapshot(equity_snapshot)

class Equity():
    def __init__(self, exchange, ticker):
        self.exchange = exchange
        self.ticker = ticker

if __name__ == "__main__":
    ss = ScreenScraper()
    ss.run()
        # Energy
        #stocks.append(Equity('NASDAQ', 'SCTY'))
        #stocks.append(Equity('NYSE', 'TOT'))
        #stocks.append(Equity('NYSE', 'XOM'))
        #stocks.append(Equity('NYSE', 'CVX'))
        #stocks.append(Equity('NYSE', 'PSX'))

        # Industrial
        #stocks.append(Equity('NYSE', 'GE'))
        #stocks.append(Equity('NYSE', 'MMM'))
        #stocks.append(Equity('NYSE', 'CAT'))
        #stocks.append(Equity('NYSE', 'DD'))

        # Technology
        #stocks.append(Equity('NASDAQ', 'AKAM'))
        #stocks.append(Equity('NYSE', 'IBM'))
        #stocks.append(Equity('NYSE', 'SAP'))
        #stocks.append(Equity('NASDAQ', 'AAPL'))
        #stocks.append(Equity('NASDAQ', 'CSCO'))
        #stocks.append(Equity('NASDAQ', 'INTC'))
        #stocks.append(Equity('NASDAQ', 'MSFT'))
        #stocks.append(Equity('NYSE', 'UTX'))
        #stocks.append(Equity('NYSE', 'NEWR'))

        # Misc
        #stocks.append(Equity('NYSE', 'SVU'))
        #stocks.append(Equity('NYSE', 'DIS'))
        #stocks.append(Equity('NYSE', 'BA'))
        #stocks.append(Equity('NYSE', 'HD'))
        #stocks.append(Equity('NYSE', 'KO'))
        #stocks.append(Equity('NYSE', 'MCD'))
        #stocks.append(Equity('NYSE', 'NKE'))
        #stocks.append(Equity('NYSE', 'TRV'))
        #stocks.append(Equity('NYSE', 'WMT'))

        # Automotive
        #stocks.append(Equity('NASDAQ', 'TSLA'))
        #stocks.append(Equity('ETR', 'VOW'))
        #stocks.append(Equity('NYSE', 'F'))

        # Communications
        #stocks.append(Equity('NYSE', 'T'))
        #stocks.append(Equity('NYSE', 'VZ'))

        # Media
        #stocks.append(Equity('NASDAQ', 'NFLX'))

        # Financial
        #stocks.append(Equity('NYSE', 'JPM'))
        #stocks.append(Equity('NYSE', 'WFC'))
        #stocks.append(Equity('NYSE', 'GS'))
        #stocks.append(Equity('NYSE', 'AXP'))
        #stocks.append(Equity('NYSE', 'V'))

        # Pharma
        #stocks.append(Equity('NYSE', 'PFE'))
        #stocks.append(Equity('NYSE', 'MRK'))

        # Health
        #stocks.append(Equity('NYSE', 'JNJ'))
        #stocks.append(Equity('NYSE', 'UNH'))
        #stocks.append(Equity('NYSE', 'PG'))

