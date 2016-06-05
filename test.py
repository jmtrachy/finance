import dal

equities = dal.EquityDAO.get_equity_snapshots_by_ticker('SCTY')
for equity in equities:
    print(str(equity.price) + ' = ' + str(equity.date))
