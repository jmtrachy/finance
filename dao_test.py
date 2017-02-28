from dao import DAO
from domain import Equity
import json

equity_ticker = 'JT_TEST'
equity_exchange = 'TJE'
equity_name = 'James Test Equity'
equity_industry = 'Industrial James'
equity_dow = True
equity_sp = True

e = Equity(None, equity_ticker, equity_name, equity_exchange, equity_industry, equity_dow, equity_sp)
dao = DAO()

print('Creating a test equity')
e = dao.create_equity(e)
print('Created the following equity: ' + json.dumps(e.__dict__))
print('Passed\r\n')

print('Retrieving all equities')
equities = dao.get_all_equities()
found_test_equity = False
for j in equities:
    print(json.dumps(j.__dict__))
    if j.equity_id == e.equity_id:
        found_test_equity = True
print('Done retrieving equities - found ' + str(len(equities)) + ' equities')
if found_test_equity:
    print('Passed')
else:
    print('Failed!!!!')

print('Retrieving equities by filter \'dow\'')
equities = dao.get_dow_equities()
found_test_equity = False
for j in equities:
    print(json.dumps(j.__dict__))
    if j.equity_id == e.equity_id:
        found_test_equity = True
print('Done retrieving equities - found ' + str(len(equities)) + ' equities')
if found_test_equity:
    print('Passed')
else:
    print('Failed!!!!')

