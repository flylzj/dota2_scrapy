# dota2_scrapy

```
git clone https://git.coding.net/flylzj/dota2_scrapy.git
```

```
cd dota2_scrapy
```

## 配置数据库 setting.py

```
MYSQL_HOST = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DB = ""
```

## 初始化数据库
```
python3 db.py
```

## 部署docker

```
sudo docker build -t dota2/scrapy
```

## 运行
```
sudo docker-compose up -d
```