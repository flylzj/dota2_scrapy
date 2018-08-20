# coding: utf-8
import scrapy
from dota2_scrapy.items import DotaHistory
import re
import json
import requests
import os
from bs4 import BeautifulSoup


class c5game_history(scrapy.Spider):
    name = "c5game_history"
    custom_settings = {
            'ITEM_PIPELINES' : {
            'dota2_scrapy.pipelines.C5gameHistoryPipeline': 300,
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
            item = DotaHistory()
            href = "https://www.c5game.com" + i.css('p.name > a::attr(href)').extract()[0]
            item["item_name"] = i.css('p.name > a > span::text').extract()[0]
            item["item_id"] = re.search(r'[0-9]*-S', href).group().strip("-S")
            histroy_url = "https://www.c5game.com/dota/history/{}.html".format(item["item_id"])
            yield scrapy.Request(histroy_url, callback=self.get_histroy, meta={"item": item})

    def get_histroy(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"class": "table sale-item-table sale-record-group"})
        trs = table.find_all("tr")
        for tr in trs:
            try:
                price = tr.find("span", attrs={"class": "ft-gold"}).text
                deal_time = tr.find("td", attrs={"style": "padding:10px 30px;"}).text
                item["price"] = price
                item["deal_time"] = deal_time
                yield item
            except AttributeError:
                pass








