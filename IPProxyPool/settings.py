#在配置文件：settings.py中定义MAX_SCORE = 50，表示代理ip的默认最高分数
MAX_SCORE = 50

#日志的配置信息
import logging
#默认配置
LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

#测试代理IP的超时时间
TEST_TIMEOUT = 10

#MongoDB数据库的URL
MONGO_URL= 'mongodb://127.0.0.1:27017'

PROXIES_SPIDERS = [
    #爬虫的全类名，路径：模块.类名
    'core.proxy_spider.proxy_spiders.XiciSpider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.IP66Spider'
]

#修改配置文件，增加爬虫运行时间间隔的配置，单位为小时

RUN_SPIDERS_INTERVAL = 2

# 配置检测代理IP的异步数量
TEST_PROXIES_ASYNC_COUNT = 10

#配置检测代理IP的时间间隔
TEST_PROXIES_INTERVAL = 2

#配置获取的代理IP的最大数量；这个值越小，可用性越高，但是随机性越差
PROXIES_MAX_COUNT = 50

