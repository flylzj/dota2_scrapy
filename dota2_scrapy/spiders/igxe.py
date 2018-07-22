# coding: utf-8
import scrapy
from dota2_scrapy.items import Dota2ScrapyItem
import json


class igxe(scrapy.Spider):
    name = "igxe"

    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "need_proxy": False
    }

    def start_requests(self):
        for i in range(1, 493):
            url = "https://www.igxe.cn/dota2/570?page_no={}".format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        url = "https://www.igxe.cn"
        items = response.xpath('//*[@id="center"]/div/div[3]/div/div[2]/div')
        for i in items:
            item = Dota2ScrapyItem()
            item["item_type"] = "igxe"
            item_href = url + i.css("div.name > a::attr(href)").extract()[0]
            item_name = i.css("div.name > a::attr(title)").extract()[0]
            item_id = item_href.split("/")[-1]
            item["item_id"] = item_id
            item["item_name"] = item_name
            item["item_href"] = item_href
            page_num = 1
            api = "https://www.igxe.cn/product/trade/570/{}?page_no={}".format(item_id, page_num)
            yield scrapy.Request(api, meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy"), "dont_redirect": True, "api": url}, callback=self.get_sale_price)

    def get_sale_price(self, response):
        item = response.meta["item"]
        page_num = response.meta["page_num"]
        item_id = item["item_id"]
        if response.status != 200:
            yield scrapy.Request(response.url, meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy"), "dont_redirect": True, "api": response.url}, callback=self.get_sale_price)
        if not item.get("sale_prices"):
            item["sale_prices"] = []
        api_data = json.loads(response.body)
        item["sale_count"] = api_data.get("page").get("total")
        data = api_data.get("d_list")
        if data:
            for d in data:
                price = d.get("unit_price")
                if price:
                    item["sale_prices"].append(price)
            page_num += 1
            api = "https://www.igxe.cn/product/trade/570/{}?page_no={}".format(item_id, page_num)
            yield scrapy.Request(api, meta={"item": item, "page_num": page_num, "need_proxy": self.custom_settings.get("need_proxy")}, callback=self.get_sale_price)
        else:
            item["purchase_prices"] = "[]"
            item["purchase_count"] = 0
            yield item









