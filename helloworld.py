import httplib
from xml.dom.minidom import parse, parseString


class ScreenScraper():
    def __init__(self, equities):
        self.equities = equities

    def run(self):
        for equity in self.equities:
            screen_scrape = self.request_equity(equity)
            self.parse_equity(equity, screen_scrape)


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


class Equity():
    def __init__(self, exchange, ticker):
        self.exchange = exchange
        self.ticker = ticker

if __name__ == "__main__":
    #h1.request("GET", '/finance?q=NASDAQ%3ASCTY')
    #h1.request("GET", '/finance?q=NYSE%3AIBM')
    #h1.request("GET", '/finance?q=NYSE%3ASVU')
    #h1.request("GET", '/finance?q=ETR%3AVOW')
    #h1.request("GET", '/finance?q=NYSE%3ADIS')
    #h1.request("GET", '/finance?q=NYSE%3AT')
    #h1.request("GET", '/finance?q=NYSE%3AGE')
    #h1.request("GET", '/finance?q=NASDAQ%3ANFLX')
    stocks = []
    stocks.append(Equity('NYES', 'GE'))
    stocks.append(Equity('NASDAQ', 'SCTY'))
    stocks.append(Equity('NYSE', 'IBM'))
    stocks.append(Equity('NYSE', 'SVU'))
    stocks.append(Equity('ETR', 'VOW'))
    stocks.append(Equity('NYSE', 'DIS'))
    stocks.append(Equity('NYSE', 'T'))
    stocks.append(Equity('NASDAQ', 'NFLIX'))


    ss = ScreenScraper(stocks)
    ss.run()
