# coding: utf-8

from dota2_scrapy.proxy import Proxy
import logging


class http_proxy_middlewares(object):
    def __init__(self):
        pass

    def process_request(self, request, spider):
        try:
            need_proxy = request.meta["need_proxy"]
        except Exception:
            need_proxy = None
        if need_proxy:
            p = Proxy()
            proxies = p.get_proxies()
            proxy = proxies[0]
            request.meta["proxy"] = proxy["proxy"]
            logging.info("正在使用{}".format(proxy["proxy"]))
        else:
            pass
            # logging.info("不需要使用代理")


