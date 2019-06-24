<h1>JD-Comments-Spider</h1>
爬取京东iPhone XR评论数据，可爬取2.4万条    

### 运行环境

python 3.x  
Ubuntu or Mac


### 如何使用

#### 安装 Redis
项目数据库使用了 [Redis](https://redis.io/)，Redis 是一个开源（BSD 许可）的，内存中的数据结构存储系统，它可以用作数据库、缓存和消息中间件。所以请确保运行环境已经正确安装了 Redis。安装方法请参照官网指南。


#### 安装依赖
使用 requirements.txt
```bash
$ pip install -r requirements.txt
```

#### 配置IP池参数
配置文件 config.py，保存了IP池所使用到的所有配置项。如下所示，用户可以根据需求自行更改。不然按默认即可。
```python
#!/usr/bin/env python
# coding=utf-8

# 请求超时时间（秒）
REQUEST_TIMEOUT = 15
# 请求延迟时间（秒）
REQUEST_DELAY = 0

# redis 地址
REDIS_HOST = "localhost"
# redis 端口
REDIS_PORT = 6379
# redis 密码
REDIS_PASSWORD = None
# redis set key
REDIS_KEY = "proxies:ranking"
# redis 连接池最大连接量
REDIS_MAX_CONNECTION = 20

# REDIS SCORE 最大分数
MAX_SCORE = 10
# REDIS SCORE 最小分数
MIN_SCORE = 0
# REDIS SCORE 初始分数
INIT_SCORE = 9

# server web host
SERVER_HOST = "localhost"
# server web port
SERVER_PORT = 4567
# 是否开启日志记录
SERVER_ACCESS_LOG = True

# 批量测试数量
VALIDATOR_BATCH_COUNT = 256
# 校验器测试网站，可以定向改为自己想爬取的网站，如新浪，知乎等
VALIDATOR_BASE_URL = "https://item.jd.com/100000177770.html"
# 校验器循环周期（分钟）
VALIDATOR_RUN_CYCLE = 15


# 爬取器循环周期（分钟）
CRAWLER_RUN_CYCLE = 30
# 请求 headers
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
```

### 运行项目

**启动IP池**
```bash
$ python3 client.py
```

```bash
$ python3 server_sanic.py
[2018-05-16 23:36:22 +0800] [108] [INFO] Goin' Fast @ http://localhost:4567
[2018-05-16 23:36:22 +0800] [108] [INFO] Starting worker [108]
```
**启动爬虫**
```bash
$ python3 spider.py
```

**储存CSV**
```bash
$ python3 process.py
```

### 参考借鉴项目

* [async-proxy-pool](https://github.com/chenjiandongx/async-proxy-pool)


