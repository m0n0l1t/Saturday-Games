from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///cool.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Town(Base):
    __tablename__ = 'town'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    first_literal = Column(String)
    is_used = Column(Integer, default=0)
    is_last = Column(Integer, default=0)

    def __init__(self, name, first_literal, is_used, is_last):
        self.name = name
        self.first_literal = first_literal
        self.is_used = is_used
        self.is_last = is_last


class Literals(Base):
    __tablename__ = 'literals'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer)

    def __init__(self, name, count):
        self.name = name
        self.count = count




def db():
    Base.metadata.create_all(engine)

