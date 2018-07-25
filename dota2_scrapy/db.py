# coding: utf-8
import os, sys
sys.path.append(os.getcwd())
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from dota2_scrapy import settings
from sqlalchemy import create_engine

engine = create_engine(settings.MYSQL_URI)
Base = declarative_base(bind=engine)


class igxe(Base):

    __tablename__ = "igxe"

    item_id = Column(Integer, primary_key=True, nullable=False, default=0)
    item_name = Column(String(255), nullable=False)
    item_href = Column(String(60), nullable=False)
    sale_prices = Column(Text, nullable=False, default="[]")
    sale_count = Column(Integer, nullable=False, default=0)
    purchase_prices = Column(Text, nullable=False, default="[]")
    purchase_count = Column(Integer, nullable=False, default=0)


class c5game(Base):

    __tablename__ = "c5game"

    item_id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    item_href = Column(String(60), nullable=False)
    sale_prices = Column(Text, nullable=False)
    sale_count = Column(Integer, nullable=False)
    purchase_prices = Column(Text, nullable=False)
    purchase_count = Column(Integer, nullable=False)


class v5fox(Base):

    __tablename__ = "v5fox"

    item_id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    item_href = Column(String(60), nullable=False)
    sale_prices = Column(Text, nullable=False)
    sale_count = Column(Integer, nullable=False)
    purchase_prices = Column(Text, nullable=False)
    purchase_count = Column(Integer, nullable=False)


class wybuff(Base):

    __tablename__ = "wybuff"

    item_id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    item_href = Column(String(60), nullable=False)
    sale_prices = Column(Text, nullable=False)
    sale_count = Column(Integer, nullable=False)
    purchase_prices = Column(Text, nullable=False)
    purchase_count = Column(Integer, nullable=False)


if __name__ == '__main__':

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
