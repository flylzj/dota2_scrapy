# coding: utf-8
import scrapy
from scrapy.loader import ItemLoader
from dota2_scrapy.items import Dota2ScrapyItem
import re
import json

class v5fox(scrapy.Spider):
    name = "v5fox"

    allow_domains = ["v5fox.com"]

    def start_requests(self):
        u = "https://www.v5fox.com/dota2?pageNum={}&pageSize=25"
        for i in range(1, 100):
            url = u.format(i)
            yield scrapy.Request(url, callback=self.get_items)

    def get_items(self, response):
        items = response.xpath("/html/body/div[6]/div[3]/div[2]/a")
        for i in items:
            item = Dota2ScrapyItem()
            item["item_type"] = "v5fox"
            href = i.css("a::attr(href)").extract()[0]
            item["item_id"] = href.strip("/dota2/item-")
            item["item_name"] = i.css("a::attr(title)").extract()[0]
            item["item_href"] = "https://www.v5fox.com" + href
            page_num = 1
            sale_api = "https://www.v5fox.com/api/item/sale?goodsItemId={}&pageNum={}&pageSize=10".format(item["item_id"], page_num)
            yield scrapy.Request(sale_api, meta={"item": item, "page_num": page_num}, callback=self.get_sale_prices)

    def get_sale_prices(self, response):
        item = response.meta["item"]
        page_num = response.meta["page_num"]

        api_data = json.loads(response.body)
        if not item.get("sale_prices"):
            item["sale_prices"] = []
            item["sale_count"] = api_data.get("totalCount")
        pages = api_data.get("pages")
        data = api_data.get("object")
        if data:
            for d in data:
                price = d.get("salePrice")
                item["sale_prices"].append(price)
        if page_num <= pages:
            page_num += 1
            sale_api = "https://www.v5fox.com/api/item/sale?goodsItemId={}&pageNum={}&pageSize=10".format(
                item["item_id"], page_num)
            yield scrapy.Request(sale_api, meta={"item": item, "page_num": page_num}, callback=self.get_sale_prices)
        else:
            page_num = 1
            purchase_api = "https://www.v5fox.com/api/item/purchase"
            body = {
                "goodsItemId": item["item_id"],
                "pageNum": str(page_num),
                "pageSize": "10"
            }

            yield scrapy.FormRequest(purchase_api, meta={"item": item, "page_num": page_num}, formdata=body, callback=self.get_purchase_prices)

    def get_purchase_prices(self, response):
        item = response.meta["item"]
        page_num = response.meta["page_num"]

        api_data = json.loads(response.body)
        if not item.get("purchase_prices"):
            item["purchase_prices"] = []
            item["purchase_count"] = api_data.get("totalCount")
        pages = api_data.get("pages")
        data = api_data.get("object")
        if data:
            for d in data:
                price = d.get("price")
                item["purchase_prices"].append(price)

        if page_num < pages:
            page_num += 1
            purchase_api = "https://www.v5fox.com/api/item/purchase"
            body = {
                "goodsItemId": item["item_id"],
                "pageNum": str(page_num),
                "pageSize": "10"
            }

            yield scrapy.FormRequest(purchase_api, meta={"item": item, "page_num": page_num}, formdata=body,
                                     callback=self.get_purchase_prices)
        else:
            yield item







