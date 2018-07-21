# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dota2ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()\
    item_type = scrapy.Field()
    item_id = scrapy.Field()
    item_name = scrapy.Field()
    item_href = scrapy.Field()
    sale_prices = scrapy.Field()
    sale_count = scrapy.Field()
    purchase_prices = scrapy.Field()
    purchase_count =scrapy.Field()


