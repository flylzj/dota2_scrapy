# coding: utf-8

import scrapy
import json
from dota2_scrapy.items import Dota2ScrapyItem
import requests


class wybuff(scrapy.Spider):
    name = "wybuff"

    allow_domains = [
        "163.com"
    ]
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        # "DOWNLOAD_DELAY" : 1,
        "need_proxy": False
    }

    def start_requests(self):
        start_url = "https://buff.163.com/api/market/goods?game=dota2&page_num={}"
        r = requests.get("https://buff.163.com/api/market/goods?game=dota2&page_num=1")
        api_data = r.json()
        page_count = api_data.get("data").get("total_page")
        for i in range(1, page_count+1):
            url = start_url.format(i)
            yield scrapy.Request(url, callback=self.get_items)

    def get_items(self, response):
        api_data = json.loads(response.text)
        datas = api_data.get("data").get("items")
        for data in datas:
            item = Dota2ScrapyItem()
            item["item_type"] = "wybuff"
            item["item_id"] = data.get("id")
            item["item_name"] = data.get("name")
            item["item_href"] = "https://buff.163.com/market/goods?goods_id={}&from=market".format(data.get("id"))
            page_num = 1
            sale_api = "https://buff.163.com/api/market/goods/sell_order?game=dota2&goods_id={}&page_num={}".format(data.get("id"), page_num)
            # print(sale_api)
            yield scrapy.Request(sale_api, meta={"item": item, "page_num": page_num}, callback=self.get_sale_prices)

    def get_sale_prices(self, response):
        item = response.meta["item"]
        if not item.get("sale_prices"):
            item["sale_prices"] = []
        page_num = response.meta["page_num"]
        try:
            api_data = json.loads(response.text)
        except Exception:
            api_data = {}
            sale_api = "https://buff.163.com/api/market/goods/sell_order?game=dota2&goods_id={}&page_num={}".format(item["item_id"], page_num)

            yield scrapy.Request(sale_api,
                                 meta={"item": item, "page_num": page_num},
                                 callback=self.get_sale_prices)
        try:
            item["sale_count"] = api_data.get("data").get("total_count")
            total_page = api_data.get("data").get("total_page")
            datas = api_data.get("data").get("items")
        except Exception:
            total_page = 0
            item["sale_count"] = 0
            datas = []
            # raise
        for data in datas:
            price = data.get("price")
            item["sale_prices"].append(price)

        if page_num <= total_page:
            page_num += 1
            sale_api = "https://buff.163.com/api/market/goods/sell_order?game=dota2&goods_id={}&page_num={}".format(item["item_id"], page_num)
            yield scrapy.Request(sale_api, meta={"item": item, "page_num": page_num}, callback=self.get_sale_prices)

        else:
            page_num = 1
            purchase_api = "https://buff.163.com/api/market/goods/buy_order?game=dota2&goods_id={}&page_num={}".format(item["item_id"], page_num)
            yield scrapy.Request(purchase_api,
                                 meta={"item": item, "page_num": page_num},
                                 callback=self.get_purchase_prices)

    def get_purchase_prices(self, response):
        item = response.meta["item"]
        if not item.get("purchase_prices"):
            item["purchase_prices"] = []
        page_num = response.meta["page_num"]
        try:
            api_data = json.loads(response.text)
        except Exception:
            api_data = {}
        try:
            item["purchase_count"] = api_data.get("data").get("total_count")
            total_page = api_data.get("data").get("total_page")
            datas = api_data.get("data").get("items")
        except Exception:
            total_page = 0
            item["purchase_count"] = 0
            datas = []
        for data in datas:
            price = data.get("price")
            item["purchase_prices"].append(price)

        if page_num < total_page:
            page_num += 1
            purchase_api = "https://buff.163.com/api/market/goods/buy_order?game=dota2&goods_id={}&page_num={}".format(item["item_id"], page_num)
            yield scrapy.Request(purchase_api, meta={"item": item, "page_num": page_num}, callback=self.get_sale_prices)
        else:
            yield item







