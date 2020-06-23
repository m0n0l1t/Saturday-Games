from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///cool.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class City(Base):
    __tablename__ = 'Cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_used = Column(Integer, default=0)
    is_last = Column(Integer, default=0)

    def __init__(self, name, is_used, is_last):
        self.name = name
        self.is_used = is_used
        self.is_last = is_last

    def __repr__(self):
        return "<Cities('%s', '%s','%s')>" % (self.name, self.is_used, self.is_last)

