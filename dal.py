#! /usr/bin/env python
import os
import collections
import logging

# SqlAlchemy imports
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import sqlalchemy

logger = logging.getLogger(__name__)
base = declarative_base()

class EquitySnapshot(base):
    __tablename__ = 'equity_snapshot'
    snapshot_id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    name = Column(String(100))
    exchange = Column(String(10))
    date = Column(Date)
    price = Column(Float)
    price_change = Column(Float)
    price_change_percent = Column(Float)

#    def __repr__(self):
#        return '<equity_snapshot%r>' % (self.snapshot_id)


class Data(object):

    def __init__(self):
        logger.debug("Creating Data Access")
        db_engine = sqlalchemy.create_engine('mysql+mysqldb://jimbob:finance@localhost/finance')
        Session = sessionmaker(bind=db_engine)
        self.session = Session()

    def insert_stock(self, 

    def get_stock(self, ticker):
        equity = EquitySnapshot()
        # can't find a good way in sqlalchey to check if a query is empty, count shoudl work for now
        count = self.session.query(EquitySnapshot).filter(EquitySnapshot.ticker==ticker.upper()).order_by(EquitySnapshot.date.desc()).count()
        if count:
            result = self.session.query(EquitySnapshot).filter(EquitySnapshot.ticker==ticker.upper()).order_by(EquitySnapshot.date.desc())
            info = [] 
            # no more than 5 results
            if count > 5:
                count = 5
            for i in range(count):
                row = result[i]
                # use format() to convert from sqlalchemy float and date to string
                info.append('{} {}'.format(row.price, row.date))
            return {ticker: info}
        else:
            return None


if __name__ == '__main__':
    dao = Data()
    print(dao.get_stock('ibm'))
    print(dao.get_stock('notfound'))
    print(dao.get_stock('IBM'))
