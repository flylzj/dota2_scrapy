# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from dota2_scrapy import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dota2_scrapy.db import igxe, wybuff, v5fox, c5game


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

