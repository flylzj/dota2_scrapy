# coding: utf-8
from scrapy import cmdline
import sys

if __name__ == '__main__':
    path = "/".join(__file__.split("/")[0:-2])
    sys.path.append(path)
    cmdline.execute("scrapy crawl c5game".split())