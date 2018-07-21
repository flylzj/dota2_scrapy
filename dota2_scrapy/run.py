# coding: utf-8

from scrapy import cmdline

cmdline.execute("scrapy crawl c5game -o items.json".split())
# cmdline.execute("scrapy crawl igxe -o items.json".split())
# cmdline.execute("scrapy crawl v5fox -o items.json".split())
# cmdline.execute("scrapy crawl wybuff -o items.json".split())


