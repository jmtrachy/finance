__author__ = 'James Trachy'

import dal
import domain
import webtest
import time
import random
from xml.dom.minidom import parseString


class ScreenScraper():
    def run(self):
        equities_to_scrape = dal.EquityDAO.get_equities(1)

        for equity in equities_to_scrape:
            try:
                screen_scrape = self.request_equity(equity)
                equity_snapshot = self.parse_equity(equity, screen_scrape)
                self.persist_equity_snapshot(equity_snapshot)
                time.sleep(random.randint(1, 10))
            except Exception as err:
                print(type(err))
                print(err.args)
                print(err)

    def request_equity(self, equity):
        req = webtest.HttpRequest()
        req.method = webtest._method_GET
        req.host = 'www.google.com'
        req.ssl = True
        req.url = '/finance?q=' + equity.exchange + '%3A' + equity.ticker

        response = webtest.WebService.send_request(req)
        return response

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

        snapshot = domain.EquitySnapshot(None, equity.equity_id, quote_time, price, price_change, price_change_percent)

        div_index = screen_scrape.index('<table class="snap-data">')
        temp_string = screen_scrape[div_index:]
        div_close_index = temp_string.index('</table>') + 8
        xml_snippet = temp_string[:div_close_index].replace('&nbsp;', '')

        self.parse_snap_data(xml_snippet, snapshot)

        div_index = screen_scrape.index('<table class="snap-data">', div_close_index + div_index)
        temp_string = screen_scrape[div_index:]
        div_close_index = temp_string.index('</table>') + 8
        xml_snippet = temp_string[:div_close_index].replace('&nbsp;', '')

        self.parse_snap_data(xml_snippet, snapshot)

        return snapshot

    def parse_snap_data(self, xml_snippet, equity):
        dom = parseString(xml_snippet)
        children = dom.getElementsByTagName('tr')

        for tr in children:
            key = None
            value = None
            for td in tr.getElementsByTagName('td'):
                td_class = td.getAttribute('class')
                if td_class == 'key':
                    key = td.firstChild.nodeValue.strip()
                elif td_class == 'val':
                    value = td.firstChild.nodeValue.strip()

            if key is not None and value is not None:
                if key == 'P/E':
                    if value != '-':
                        equity.pe = value
                elif key == 'Div/yield':
                    if value != '-':
                        fields = value.split('/')
                        if fields[0] == '-':
                            equity.dividend = 0.0
                        else:
                            equity.dividend = fields[0]
                        equity.dividend_yield = fields[1]


    def persist_equity_snapshot(self, equity_snapshot):
        print('About to persist snapshot to service')
        print('Snapshot = ' + str(equity_snapshot))
        d = dao.DAO()
        # d.create_snapshot({ "test": 'hi' })
        d.create_snapshot(equity_snapshot)
        # EquityDAO.create_equity_snapshot(equity_snapshot)


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

