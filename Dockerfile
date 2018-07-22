FROM aciobanu/scrapy

MAINTAINER 1449902124@qq.com

RUN mkdir /app

# RUN mkdir /app/dota2_scrapy

COPY req.txt /app

VOLUME scrapy.cfg /app

RUN pip install -r /app/req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

VOLUME dota2_scrapy/ /app/

WORKDIR /app/dota2_scrapy

CMD ["python c5game_run.py"]



