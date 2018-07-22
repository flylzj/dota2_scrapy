# coding: utf-8

import requests


class Proxy(object):
    def __init__(self):
        self.url = "http://139.199.183.108:8000/"
        self.delete_url = "http://139.199.183.108:8000/delete"
        self.check_urls = {
            "wybuff": "https://buff.163.com/api/market/goods/sell_order?game=dota2&goods_id=15161&page_num=1",
            "c5game": "https://www.c5game.com/api/product/sale.json?id=805759&quick=&gem_id=0&page=1&flag=&seller=",
            "v5fox": "https://www.v5fox.com/api/item/sale?goodsItemId=1010593&pageNum=1&pageSize=10",
            "igxe": "https://www.igxe.cn/product/trade/570/611660"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

    def get_proxies(self, count=1):
        proxies = []
        r = requests.get(self.url)
        if r.text:
            datas = eval(r.text)
        else:
            datas = []
        for data in datas:
            p = {}
            p["proxy"] = "https://{}:{}".format(data[0], data[1])
            p["ip"] = data[0]
            proxies.append(p)
        return proxies

    def delete_proxy(self, proxy):
        ip = proxy.get("ip")
        params = {
            "ip": ip
        }
        try:
            r = requests.get(self.delete_url, params=params)
        except Exception:
            pass
        return True

    def check_proxy(self, t):
        url = self.check_urls.get(t)
        try:
            r = requests.get(url, headers=self.headers, timeout=3)
            r.json()
            if r.status_code != 200:
                return False
        except Exception:
            return False
        return True

