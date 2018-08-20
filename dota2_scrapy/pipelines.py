# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dota2_scrapy import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dota2_scrapy.db import igxe, wybuff, v5fox, c5game, history


class Dota2ScrapyPipeline(object):

    def __init__(self):
        mysql_uri = settings.MYSQL_URI
        engine = create_engine(mysql_uri, pool_size=100)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        item_type = item["item_type"]
        self.dom_info(item_type, item)
        return item

    def dom_info(self, item_type, item):
        session = self.Session()
        table = eval(item_type)
        good = session.query(table).filter(table.item_id==item["item_id"]).first()
        if good:
            good.sale_prices = str(item["sale_prices"])
            good.sale_count = item["sale_count"]
            good.purchase_prices = str(item["purchase_prices"])
            good.purchase_count = item["purchase_count"]
            session.commit()
            session.close()
            return

        i = table(
            item_id=item["item_id"],
            item_name=item["item_name"],
            item_href=item["item_href"],
            sale_prices=str(item["sale_prices"]),
            sale_count=item["sale_count"],
            purchase_prices=str(item["purchase_prices"]),
            purchase_count=item["purchase_count"]
        )
        session.add(i)
        session.commit()
        session.close()
        return


class C5gameHistoryPipeline(object):
    def __init__(self):
        mysql_uri = settings.MYSQL_URI
        engine = create_engine(mysql_uri, pool_size=100)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        item = self.deal_item(item)
        self.dom_info(item)
        return item

    def deal_item(self, item):
        try:
            item["price"] = float(item["price"].strip("￥"))
            item["deal_time"] = item["deal_time"].strip()
        except Exception as e:
            print(e)
            item["price"] = 0
            item["deal_time"] = "1900-00-00 00:00:00"
        return item

    def dom_info(self, item):
        session = self.Session()
        i = session.query(history).filter_by(
            deal_time=item["deal_time"]
        ).first()
        if i:
            print("已存在")
            return
        i = history(
            item_id=item["item_id"],
            item_name=item["item_name"],
            price=item["price"],
            deal_time=item["deal_time"]
        )
        session.add(i)
        session.commit()
        session.close()




