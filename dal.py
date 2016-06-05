import MySQLdb


class Equity():
    def __init__(self, equity_id, ticker, name, exchange, industry):
        self.equity_id = equity_id
        self.ticker = ticker
        self.name = name
        self.exchange = exchange 
        self.industry = industry


class EquitySnapshot():
    def __init__(self, snapshot_id, equity_id, date, price, price_change, price_change_percent):
        self.snapshot_id = snapshot_id
        self.equity_id = equity_id
        self.date = date
        self.price = price
        self.price_change = price_change
        self.price_change_percent = price_change_percent


class EquityAggregate():
    def __init__(self, aggregate_id, equity_id, date, fifty_day_moving_avg, fifty_day_volatility_avg, per_off_recent_high, per_off_recent_low):
        self.aggregate_id = aggregate_id
        self.equity_id = equity_id
        self.date = date    
        self.fifty_day_moving_avg = fifty_day_moving_avg
        self.fifty_day_volatility_avg = fifty_day_volatility_avg
        self.per_off_recent_high = per_off_recent_high
        self.per_off_recent_low = per_off_recent_low 


class EquityDAO():

    # The select equity query and hydration function for the query
    __SELECT_EQUITY_BASE = 'SELECT e.`equity_id`, e.`ticker`, e.`name`, e.`exchange`, e.`industry`' +\
                           '  FROM `equity` e'

    @staticmethod
    def __hydrate_equity(row):
        return Equity(row[0], row[1], row[2], row[3], row[4])

    __SELECT_EQUITY_SNAPSHOT_BASE = 'SELECT es.`snapshot_id`, es.`equity_id`, es.`date`, es.`price`, es.`price_change`, es.`price_change_percent` ' +\
                                    '  FROM `equity_snapshot` es'

    @staticmethod
    def __hydrate_equity_snapshot(row):
        return EquitySnapshot(row[0], row[1], row[2], row[3], row[4], row[5])

    @staticmethod
    def __get_connection():
        cnx = MySQLdb.connect(host='localhost', # your host, usually localhost
                              user='jimbob', # your username
                              passwd='finance', # your password
#                              db='finance') # name of the data base
                              db='jt_test')
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
        
        return EquityDAO.__execute_select(select_equity_by_id, query_data, EquityDAO.__hydrate_equity)

    @staticmethod
    def create_equity(equity):
        insert_equity = 'INSERT INTO `equity` (`ticker`, `name`, `exchange`, `industry`) VALUES (%s, %s, %s, %s)'
        query_data = equity.ticker, equity.name, equity.exchange, equity.industry

        EquityDAO.__execute_insert(insert_equity, query_data, equity)

    @staticmethod
    def create_equity_snapshot(equity_snapshot):
        insert_equity_snapshot = 'INSERT INTO `equity_snapshot` (`equity_id`, `date`, `price`, `price_change`, `price_change_percent`) VALUES (%s, %s, %s, %s, %s)'
        query_data = equity_snapshot.equity_id, equity_snapshot.date, equity_snapshot.price, equity_snapshot.price_change, equity_snapshot.price_change_percent

        EquityDAO.__execute_insert(insert_equity_snapshot, query_data, equity_snapshot)

    @staticmethod
    def create_equity_aggregate(equity_aggregate):
        insert_equity_aggregate = 'INSERT INTO `equity_aggregate` (`equity_id`, `fifty_day_moving_avg`, `fifty_day_volatility_avg`, `per_off_recent_high`, `per_off_recent_low`) VALUES (%s, %s, %s, %s, %s)'
        query_data = equity_aggregate.equity_id, equity_aggregate.fifty_day_moving_avg, equity_aggregate.fifty_day_volatility_avg, equity_aggregate.per_off_recent_high, equity_aggregate.per_off_recent_low

        EquityDAO.__execute_insert(insert_equity_aggregate, query_data, equity_aggregate)

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
        select_equities = EquityDAO.__SELECT_EQUITY_BASE + ' ORDER BY `name` ASC LIMIT %s'
        query_data = limit

        equities = EquityDAO.__execute_select(select_equities, query_data, EquityDAO.__hydrate_equity) 
        return equities
