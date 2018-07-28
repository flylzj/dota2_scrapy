# coding: utf-8
import scrapy
from dota2_scrapy.items import Dota2ScrapyItem
import re
import json
import requests
import os


class c5game(scrapy.Spider):
    name = "c5game"
    custom_settings = {
        "CONCURRENT_REQUESTS": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "need_proxy": False,
        "DOWNLOAD_DELAY": 1,
        "PROXY_MODE": 0,
        "PROXY_LIST": os.getcwd() + "/proxy.txt",
        "RETRY_HTTP_CODES": [500, 503, 504, 400, 403, 404, 408, 429],
        "RETRY_TIMES": 100,
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy_proxies.RandomProxy': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }
    }

    def start_requests(self):
        u = "https://www.c5game.com/dota.html?page={}"
        r = requests.get("https://www.c5game.com/dota.html")
        tmp = re.findall(r'\?page=[0-9]{1,3}', r.text)[-1]
        page = int(tmp.strip("?page="))

        for i in range(1, page + 1):
            url = u.format(i)
            yield scrapy.Request(url, callback=self.get_items)

    def get_items(self, response):
        items = response.xpath('//*[@id="yw0"]/div[1]/ul/li')

        for i in items:
            item = Dota2ScrapyItem()
            item["item_type"] = "c5game"
            item["item_href"] = "https://www.c5game.com" + i.css('p.name > a::attr(href)').extract()[0]
            item["item_name"] = i.css('p.name > a > span::text').extract()[0]
            yield scrapy.Request(item["item_href"], meta={"item": item}, callback=self.get_item_api)

    def get_item_api(self, response):
        item = response.meta["item"]
        api = response.css("#sale-body::attr(data-url)")[0].extract()
        item_id = re.search(r'id=[0-9]*', api).group().strip("id=")
        item["item_id"] = item_id
        page_num = 1
        api = "https://www.c5game.com/api/product/sale.json?id={}&page={}".format(item_id, page_num)
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }
        yield scrapy.Request(api, meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy"), "api": api}, headers=headers, callback=self.get_sale_prices)

    def get_sale_prices(self, response):
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }
        item = response.meta["item"]
        item_id = item["item_id"]
        page_num = response.meta["page_num"]
        if not item.get("sale_prices"):
            item["sale_prices"] = []
        api_data = json.loads(response.text)
        data = api_data.get("body")
        if not data:
            yield scrapy.Request(response.url,
                                 meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy")},
                                 headers=headers, callback=self.get_sale_prices
            )
        more = data.get("more")
        items = data.get("items")
        for i in items:
            price = i.get("price")
            item["sale_prices"].append(price)
        # print(more)
        if more == 1:
            page_num += 1
            api = "https://www.c5game.com/api/product/sale.json?id={}&page={}".format(item_id, page_num)
            yield scrapy.Request(api,
                                 meta={"item": item, "page_num": page_num, "api": api, "need_proxy": self.custom_settings.get("need_proxy")},
                                 headers=headers, callback=self.get_sale_prices)
        elif more == 0:
            page_num = 1
            api = "https://www.c5game.com/api/product/purchase.json?id={}&page={}".format(item["item_id"], 1)
            # print("api", api)
            item["sale_count"] = len(item["sale_prices"])
            yield scrapy.Request(api,
                                 meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy"), "api": api},
                                 headers=headers, callback=self.get_purchase_prices)

    def get_purchase_prices(self, response):
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }
        item = response.meta["item"]
        item_id = item["item_id"]
        page_num = response.meta["page_num"]
        if not item.get("purchase_prices"):
            item["purchase_prices"] = []
        api_data = json.loads(response.text)
        data = api_data.get("body")
        try:
            more = data.get("more")
            items = data.get("items")
            # print("pur", more)
            for i in items:
                price = i.get("price")
                item["purchase_prices"].append(price)
            if more == 1:
                page_num += 1
                api = "https://www.c5game.com/api/product/purchase.json?id={}&page={}".format(item_id, page_num)
                yield scrapy.Request(api,
                                     meta={"item": item, "page_num": page_num, "api": api, "need_proxy": self.custom_settings.get("need_proxy")},
                                     headers=headers, callback=self.get_purchase_prices)
            else:
                item["purchase_count"] = len(item["purchase_prices"])
                yield item
        except Exception:
            item["purchase_count"] = len(item["purchase_prices"])
            yield item















