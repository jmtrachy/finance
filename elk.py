from dal import EquityDAO
import httplib

equities = EquityDAO.get_equities()
for e in equities:
 
    snapshots = EquityDAO.get_equity_snapshots_by_ticker(e.ticker, 100)

    for s in snapshots:
        if s.dividend is None:
            dividend = 0.0
            dividend_yield = 0.0
        else:
            dividend = s.dividend
            dividend_yield = s.dividend_yield

        if s.pe is None:
            pe = -1
        else:
            pe = s.pe
    
        if e.dow is None:
            dow = False
        else:
            dow = e.dow
    
        if e.industry is None:
            industry = ''
        else:
            industry = e.industry
    
        message = '"ticker": "{}", "date": "{}", "sector": "{}", "dow": "{}", "name": "{}", "price": "{}", "price_change": "{}", "price_change_percent": "{}", "dividend": "{}", "dividend_yield": "{}", "pe": "{}"'.format(e.ticker, s.date, industry, dow, e.name, s.price, s.price_change, s.price_change_percent, dividend, dividend_yield, pe)
        message = '{' + message + '}'
    
    
        conn = httplib.HTTPConnection('54.197.44.172:9200')
        log_url = '/finance/snapshot?pretty'
    
        headers = {}
        headers['Content-Length'] = len(message)
        headers['Content-Type'] = 'application/json'
    
        conn.request('POST', log_url, message)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')

        if response.status > 299:
            print('message = ' + message)
            print(response_data)
    
        conn.close()
