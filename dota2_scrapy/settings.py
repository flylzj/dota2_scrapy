# -*- coding: utf-8 -*-

BOT_NAME = 'dota2_scrapy'

SPIDER_MODULES = ['dota2_scrapy.spiders']
NEWSPIDER_MODULE = 'dota2_scrapy.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
MYSQL_HOST = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DB = ""
MYSQL_URI = "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32


CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

RETRY_TIMES = 10

SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror': None,
    'scrapy.downloadermiddlewares.redirect': None
}

RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOADER_MIDDLEWARES = {
    'dota2_scrapy.proxymid.http_proxy_middlewares': 100
}
PROXY_LIST = "C:\\Users\\lzj\\proxy.txt"
PROXY_MODE = 0

ITEM_PIPELINES = {
   'dota2_scrapy.pipelines.Dota2ScrapyPipeline': 300,
}
