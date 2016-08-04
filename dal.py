import MySQLdb
import myconfig


class Equity():
    def __init__(self, equity_id, ticker, name, exchange, industry, dow):
        self.equity_id = equity_id
        self.ticker = ticker
        self.name = name
        self.exchange = exchange 
        self.industry = industry
        self.snapshots = []
        self.aggregates = []
        self.dow = dow


class EquitySnapshot():
    def __init__(self, snapshot_id, equity_id, date, price, price_change, price_change_percent, dividend=None, dividend_yield=None, pe=None):
        self.snapshot_id = snapshot_id
        self.equity_id = equity_id
        self.date = date
        self.price = price
        self.price_change = price_change
        self.price_change_percent = price_change_percent
        self.dividend = dividend
        self.dividend_yield = dividend_yield
        self.pe = pe


class EquityAggregate():
    def __init__(self, aggregate_id, equity_id, date, fifty_day_moving_avg, fifty_day_volatility_avg, per_off_recent_high, per_off_recent_low):
        self.aggregate_id = aggregate_id
        self.equity_id = equity_id
        self.date = date    
        self.fifty_day_moving_avg = fifty_day_moving_avg
        self.fifty_day_volatility_avg = fifty_day_volatility_avg
        self.per_off_recent_high = per_off_recent_high
        self.per_off_recent_low = per_off_recent_low 
        self.ticker = None

    def set_ticker(ticker):
        self.ticker = ticker


class EquityMeta():
    def __init__(self, ticker, num_days_tracked):
        self.ticker = ticker
        self.num_days_tracked = num_days_tracked


class EquityDAO():

    # The select equity query and hydration function for the query
    __SELECT_EQUITY_BASE = 'SELECT e.`equity_id`, e.`ticker`, e.`name`, e.`exchange`, e.`industry`, e.`dow`' +\
                           '  FROM `equity` e'

    @staticmethod
    def __hydrate_equity(row):
        return Equity(row[0], row[1], row[2], row[3], row[4], row[5])

    __SELECT_EQUITY_SNAPSHOT_BASE = 'SELECT es.`snapshot_id`, es.`equity_id`, es.`date`, es.`price`, es.`price_change`, es.`price_change_percent` , es.`dividend`, ' +\
                                    '       es.`dividend_yield`, es.`pe` ' +\
                                    '  FROM `equity_snapshot` es'

    @staticmethod
    def __hydrate_equity_snapshot(row):
        return EquitySnapshot(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    __SELECT_EQUITY_AGGREGATE_BASE = 'SELECT ea.`aggregate_id`, ea.`equity_id`, ea.`date`, ea.`fifty_day_moving_avg`, ea.`fifty_day_volatility_avg`, ea.`per_off_recent_high`, ea.`per_off_recent_low` ' +\
                                    '  FROM `equity_aggregate` ea '

    @staticmethod
    def __hydrate_equity_meta(row):
        return EquityMeta(row[0], row[1])

    @staticmethod
    def __hydrate_equity_aggregate(row):
        return EquityAggregate(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    @staticmethod
    def __get_connection():
        host = myconfig.db_host
        user = myconfig.db_user
        passwd = myconfig.db_passwd
        schema = myconfig.db_schema
        cnx = MySQLdb.connect(host=host, # your host, usually localhost
                              user=user, # your username
                              passwd=passwd, # your password
                              db=schema) # name of the data base
#                              db='jt_test')
        return cnx

    @staticmethod
    def __get_cursor(cnx):
        cursor = cnx.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        return cursor

    @staticmethod
    def get_equity_snapshots_by_ticker(ticker, limit=50):
        query = EquityDAO.__SELECT_EQUITY_SNAPSHOT_BASE + ' JOIN `equity` e ON es.`equity_id` = e.`equity_id` WHERE e.`ticker` = %s ORDER BY es.`date` DESC LIMIT %s'
        query_data = ticker, limit

        return EquityDAO.__execute_select(query, query_data, EquityDAO.__hydrate_equity_snapshot) 

    @staticmethod
    def get_equity_by_ticker(ticker):
        select_equity_by_ticker = EquityDAO.__SELECT_EQUITY_BASE + ' WHERE `ticker` = %s'
        query_data = ticker

        equities = EquityDAO.__execute_select(select_equity_by_ticker, query_data, EquityDAO.__hydrate_equity)
        return equities

    @staticmethod
    def get_equity_by_id(equity_id):
        select_equity_by_id = EquityDAO.__SELECT_EQUITY_BASE + ' WHERE `equity_id` = %s'
        query_data = equity_id
       
        equities = EquityDAO.__execute_select(select_equity_by_id, query_data, EquityDAO.__hydrate_equity)
        return equities[0]

    @staticmethod
    def create_equity(equity):
        insert_equity = 'INSERT INTO `equity` (`ticker`, `name`, `exchange`, `industry`) VALUES (%s, %s, %s, %s)'
        query_data = equity.ticker, equity.name, equity.exchange, equity.industry

        EquityDAO.__execute_insert(insert_equity, query_data, equity)

    @staticmethod
    def create_equity_snapshot(equity_snapshot):
        insert_equity_snapshot = 'INSERT INTO `equity_snapshot` (`equity_id`, `date`, `price`, `price_change`, `price_change_percent`, `dividend`, `dividend_yield`, `pe`) ' +\
                                 '                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        query_data = equity_snapshot.equity_id, equity_snapshot.date, equity_snapshot.price, equity_snapshot.price_change, equity_snapshot.price_change_percent, equity_snapshot.dividend, \
                     equity_snapshot.dividend_yield, equity_snapshot.pe

        EquityDAO.__execute_insert(insert_equity_snapshot, query_data, equity_snapshot)

    @staticmethod
    def create_equity_aggregate(equity_aggregate):
        insert_equity_aggregate = 'INSERT INTO `equity_aggregate` (`equity_id`, `fifty_day_moving_avg`, `fifty_day_volatility_avg`, `per_off_recent_high`, `per_off_recent_low`) VALUES (%s, %s, %s, %s, %s)'
        query_data = equity_aggregate.equity_id, equity_aggregate.fifty_day_moving_avg, equity_aggregate.fifty_day_volatility_avg, equity_aggregate.per_off_recent_high, equity_aggregate.per_off_recent_low

        EquityDAO.__execute_insert(insert_equity_aggregate, query_data, equity_aggregate)


    @staticmethod
    def get_top_equity_aggregate_by_id(equity_id):
        select_query = EquityDAO.__SELECT_EQUITY_AGGREGATE_BASE + ' WHERE ea.`equity_id` = %s ORDER BY ea.`date` DESC LIMIT 1'
        query_data = equity_id

        list_of_aggregates = EquityDAO.__execute_select(select_query, query_data, EquityDAO.__hydrate_equity_aggregate)
        aggregate_to_return = None
        if len(list_of_aggregates) > 0:
            aggregate_to_return = list_of_aggregates[0]

        return aggregate_to_return

    @staticmethod
    def get_equity_aggregates_by_ticker(ticker, limit=50):
        select_query = EquityDAO.__SELECT_EQUITY_AGGREGATE_BASE + ' JOIN `equity` e ON e.`equity_id` = ea.`equity_id` WHERE e.`ticker` = %s ORDER BY ea.`date` DESC LIMIT %s'
        query_data = ticker, limit

        return EquityDAO.__execute_select(select_query, query_data, EquityDAO.__hydrate_equity_aggregate)

    @staticmethod
    def __execute_select(query, query_data, hydration_func):
        result_objs = []
       
        #print('Query = ' + query + '; query_data = ' + str(query_data)) 
        cnx = None
        cursor = None

        try:
            cnx = EquityDAO.__get_connection()
            cursor = EquityDAO.__get_cursor(cnx)

            if query_data is None:
                cursor.execute(query)
            else:
                cursor.execute(query, query_data)
 
            results = cursor.fetchall()

            for row in results:
                result_objs.append(hydration_func(row))

        except Exception as e:
            print(type(e))
            print(e) 

        finally: 
            cursor.close()
            cnx.close()

        return result_objs

    @staticmethod
    def __execute_insert(query, query_data, record):
        print('Query = ' + query + '; query_data = ' + str(query_data))

        cnx = None
        cursor = None

        try:
            cnx = EquityDAO.__get_connection()
            cursor = EquityDAO.__get_cursor(cnx)

            cursor.execute(query, query_data)

        except Exception as e:
            print(type(e))
            print(e) 

        finally:
            cnx.commit()
            cursor.close()
            cnx.close()


    @staticmethod        
    def get_equities(limit=1000):
        select_equities = EquityDAO.__SELECT_EQUITY_BASE + ' ORDER BY `equity_id` ASC LIMIT %s'
        query_data = limit

        equities = EquityDAO.__execute_select(select_equities, query_data, EquityDAO.__hydrate_equity) 
        return equities

    @staticmethod
    def get_equity_with_most_recent_data(ticker, num_snapshots=5, num_aggregates=5):
        equity = None
        equities = EquityDAO.get_equity_by_ticker(ticker)

        if len(equities) > 0:
            equity = equities[0]
            equity.snapshots = EquityDAO.get_equity_snapshots_by_ticker(ticker, num_snapshots)
            equity.aggregates = EquityDAO.get_equity_aggregates_by_ticker(ticker, num_aggregates)

        return equity

    @staticmethod
    def get_dow_equities():
        select_equities = EquityDAO.__SELECT_EQUITY_BASE + ' WHERE `dow` = 1'
        equities = EquityDAO.__execute_select(select_equities, None, EquityDAO.__hydrate_equity)

        return equities

    @staticmethod
    def get_most_recent_snapshots(equities, sort='dividend_yield'):
        extra_where_clause = ''
        if equities is not None and len(equities) > 0:
            extra_where_clause = ' AND `equity_id` IN %s '

        query_data = sort
        if extra_where_clause != '':
            equity_ids = []
            for equity in equities:
                equity_ids.append(equity.equity_id)

            query_data = equity_ids, sort

        query = EquityDAO.__SELECT_EQUITY_SNAPSHOT_BASE + ' WHERE `snapshot_id` IN (SELECT MAX(`snapshot_id`) FROM `equity_snapshot` GROUP BY `equity_id`)' + extra_where_clause + ' ORDER BY %s' 

        return EquityDAO.__execute_select(query, query_data, EquityDAO.__hydrate_equity_snapshot)

    @staticmethod
    def get_recent_aggregates():
        query = EquityDAO.__SELECT_EQUITY_AGGREGATE_BASE + ' WHERE `aggregate_id` IN (SELECT MAX(`aggregate_id`) FROM `equity_aggregate` GROUP BY `equity_id`)'

        return EquityDAO.__execute_select(query, None, EquityDAO.__hydrate_equity_aggregate)

    @staticmethod
    def get_equity_meta():
        query = 'SELECT e.`ticker`, COUNT(es.`equity_id`) AS theCount FROM `equity_snapshot` es JOIN `equity` e ON es.`equity_id` = e.`equity_id` GROUP BY es.`equity_id` ORDER BY e.`ticker` ASC'

        return EquityDAO.__execute_select(query, None, EquityDAO.__hydrate_equity_meta)
