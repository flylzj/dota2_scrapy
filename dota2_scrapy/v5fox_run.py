# coding: utf-8
from scrapy import cmdline

if __name__ == '__main__':
    print("/".join(__file__.split("/")[0:-2]))
    cmdline.execute("scrapy crawl v5fox".split())