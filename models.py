from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import random

Base = declarative_base()
engine = create_engine('sqlite:///cool.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Town(Base):
    __tablename__ = 'town'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    first_literal = Column(String)

    def __init__(self, name, first_literal):
        self.name = name
        self.first_literal = first_literal


class Literals(Base):
    __tablename__ = 'literals'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    last = Column(Integer)
    used = Column(Integer)
    l1 = Column(Integer)
    l2 = Column(Integer)
    l3 = Column(Integer)
    l4 = Column(Integer)
    l5 = Column(Integer)
    l6 = Column(Integer)
    l7 = Column(Integer)
    l8 = Column(Integer)
    l9 = Column(Integer)
    l10 = Column(Integer)
    l11 = Column(Integer)
    l12 = Column(Integer)
    l13 = Column(Integer)
    l14 = Column(Integer)
    l15 = Column(Integer)
    l16 = Column(Integer)
    l17 = Column(Integer)
    l18 = Column(Integer)
    l19 = Column(Integer)
    l20 = Column(Integer)
    l21 = Column(Integer)
    l22 = Column(Integer)
    l23 = Column(Integer)
    l24 = Column(Integer)
    l25 = Column(Integer)
    l26 = Column(Integer)
    l27 = Column(Integer)
    l28 = Column(Integer)
    l29 = Column(Integer)

    def __init__(self, channel_id):

        last_id = random.randint(1, 10306)
        self.channel_id = channel_id
        self.last = last_id
        self.l1 = 567
        self.l2 = 902
        self.l3 = 703
        self.l4 = 441
        self.l5 = 399
        self.l6 = 96
        self.l7 = 65
        self.l8 = 169
        self.l9 = 266
        self.l10 = 30
        self.l11 = 1211
        self.l12 = 455
        self.l13 = 637
        self.l14 = 460
        self.l15 = 286
        self.l16 = 558
        self.l17 = 337
        self.l18 = 855
        self.l19 = 455
        self.l20 = 170
        self.l21 = 227
        self.l22 = 338
        self.l23 = 31
        self.l24 = 217
        self.l25 = 177
        self.l26 = 12
        self.l27 = 137
        self.l28 = 37
        self.l29 = 68


class Used(Base):
    __tablename__ = 'used'

    id = Column(Integer, primary_key=True)
    channel_id = Column(String)
    used_city = Column(Integer)

    def __init__(self, channel_id, used_city):
        self.channel_id = channel_id
        self.used_city = used_city


def db():
    Base.metadata.create_all(engine)
