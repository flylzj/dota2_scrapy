# coding: utf-8
from scrapy import cmdline
import os, sys

if __name__ == '__main__':
    print("/".join(__file__.split("/")[0:-2]))
    # cmdline.execute("scrapy crawl wybuff".split())