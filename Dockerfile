FROM aciobanu/scrapy

MAINTAINER 1449902124@qq.com

RUN mkdir /app

# RUN mkdir /app/dota2_scrapy

COPY req.txt /app

VOLUME scrapy.cfg /app

RUN pip install -r /app/req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



