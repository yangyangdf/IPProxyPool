"""
目标：
    为爬虫模块提供高可用代理IP的接口
步骤：
    1. 实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
    2. 实现根据协议类型和域名，提供获取多个高可用代理IP的服务
    3. 实现指定的IP上追加不可以域名的服务

实现：
    1.在proxy_api.py中，创建ProxyApi类
    2.实现初始方法：
        2.1初始化一个Flask的Web服务
        2.2实现根据协议类型和域名，提供随机的获取高可用的代理IP服务
            可通过protocol 和 domain 参数对Ip进行过滤
            protocol ：当前请求的协议
            domain ：当前请求域名
        2.3实现根据协议和域名，提供获取多个高可用代理的服务
            可指定potocol 和domain 参数对IP进行过滤
        2.4实现给指定的IP上追加不可用域名的服务
            如果在获取IP的时候，有指定域名参数，将不在获取该ip，从而进一步提高代理IP的可用性
    3.实现run方法，用于启动Flask的Web服务
    4.实现start的类方法，用于通过类名，启动服务
"""
import json

from flask import Flask
from flask import request
from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT


class ProxyApi(object):

    def __init__(self):
        #初始化一个Flask的Web服务
        self.app = Flask(__name__)
        #创建MongoPool对象，用于操作数据库
        self.mongo_pool = MongoPool()


        @self.app.route('/random')
        def random():
            """
            2.2实现根据协议类型和域名，提供随机的获取高可用的代理IP服务
            可通过protocol 和 domain 参数对Ip进行过滤
            protocol ：当前请求的协议
            domain ：当前请求域名
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol,domain,count=PROXIES_MAX_COUNT)

            if protocol:
                return '{}://{}:{}'.format(protocol,proxy.ip,proxy.port)
            else:
                return '{}:{}'.format(proxy.ip,proxy.port)

        @self.app.route('/proxies')
        def proxies():
            """
            2.3实现根据协议和域名，提供获取多个高可用代理的服务
                可指定potocol 和domain 参数对IP进行过滤

            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol,domain,count=PROXIES_MAX_COUNT)
            #proxies 是一个Proxy对象的列表，但是Proxy对象不能进行json序列化，需要转换成字典列表
            #转化为字典
            proxies = [proxy.__dict__ for proxy in proxies]
            #返回json字符串
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            #2.4实现给指定的IP上追加不可用域名的服务
                #如果在获取IP的时候，有指定域名参数，将不在获取该ip，从而进一步提高代理IP的可用性
            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return '情提供ip参数'
            if domain is None:
                return '情提供域名domain参数'

            self.mongo_pool.disable_domain(ip,domain)
            return '{}禁用域名{}成功'.format(ip,domain)

    def run(self):
        self.app.run(host='0.0.0.0',port=16888)

    @classmethod
    def start(cls):
        #    4.实现start的类方法，用于通过类名，启动服务
        proxy_api = cls()
        proxy_api.run()

if __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    ProxyApi.start()
