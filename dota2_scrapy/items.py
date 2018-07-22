# -*- coding: utf-8 -*-
import scrapy


class Dota2ScrapyItem(scrapy.Item):
    item_type = scrapy.Field()
    item_id = scrapy.Field()
    item_name = scrapy.Field()
    item_href = scrapy.Field()
    sale_prices = scrapy.Field()
    sale_count = scrapy.Field()
    purchase_prices = scrapy.Field()
    purchase_count =scrapy.Field()


