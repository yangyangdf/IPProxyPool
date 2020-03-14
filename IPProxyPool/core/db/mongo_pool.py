"""
实现代理池的数据库模块
作用：用于对proxies集合进行数据库的相关操作
目标：实现对数据库的增删改查相关操作
步骤：
1.在init中，建立数据库连接，获取要操作的集合，在del方法中关闭数据库

2.提供基础的增删改查功能
    2.1 实现插入功能
    2.2 实现修改功能
    2.3 实现删除代理：根据代理的IP删除代理
    2.4 查询所有代理iP的功能
"""
import random

import pymongo
from pymongo import MongoClient

from domain import Proxy
from settings import MONGO_URL
from utils.log import logger


class MongoPool(object):
    def __init__(self):
        # 1.1 在init中，建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 1.2 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 1.3 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        """2.1 实现插入的功能"""
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 我们使用proxy的ip作为MongonDB中的数据库主键：_id
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info("插入新的代理{}".format(proxy))
        else:
            logger.warning("已经存在的代理：{}".format(proxy))

    def update_one(self, proxy):
        """2.2 实现修改功能"""
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        """2.3 实现删除代理，根据代理IP删除代理"""
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("删除代理IP：{}".format(proxy))

    def find_all(self):
        """2.4 查询所有代理IP的功能"""
        cursor = self.proxies.find()
        for item in cursor:
            # 删除_id这个key
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        3.1 实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，在速度升序排
        保证优质的代理IP在上面

        :param condition: 查询条件字典
        :param count: 限制最多取出多少歌代理IP
        :return: 返回满足要求代理IP（Proxy对象）列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort(
            [('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)]
        )
        # 准备列表，用于存储查询处理代理IP
        proxy_list = []
        # 遍历cursor
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)

        # 返回满足条件要求代理IP(Proxy对象)列表
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        3.2 实现根据协议类型 和 要访问网站的域名，获取代理IP列表
        :param protocal: 协议 http,https
        :param domain: 域名：jd.com
        :param count: 用于限制获取多个代理IP，默认时获取所有
        :param nick_type: 匿名类型，默认，获取高匿名代理IP
        :return: 满足要求的代理IP
        """
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议，指定查询条件
        if protocol is None:
            # 如果没有传入协议类型，返回支持http和https的代理IP
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}
        if domain:
            conditions['disable_domains'] = {'$nin', [domain]}

        return self.find(conditions, count=count)

    def random_proxy(self,protocol=None,domain=None,nick_type=0,count=0):
        """

        :param protocal: 协议 http,https
        :param domain: 域名：jd.com
        :param count: 用于限制获取多个代理IP，默认时获取所有
        :param nick_type: 匿名类型，默认，获取高匿名代理IP
        :return: 满足要求的随机代理IP
        """
        proxy_list = self.get_proxies(protocol=protocol,domain=domain,count=count,nick_type=nick_type)
        print(proxy_list)
        print(random.choice(proxy_list))
        return random.choice(proxy_list)


    def disable_domain(self,ip,domain):
        """
        3.4 实现把指定域名添加到指定IP的disable_domain列表中
        :param ip:
        :param domain:
        :return: 如果返回Ttue，就表示添加成功了，返回False添加失败
        """
        if self.proxies.count_documents({'_id':ip,'disable_domains':domain}) == 0:
            #如果disable_damain字段中没有这个域名，才添加
            self.proxies.update_one({'_id':ip},{'$push':{'disable_domains':domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('218.27.136.170',port='8085')
    # mongo.insert_one(proxy)
    # proxy = Proxy('218.27.136.169',port='8888')
    # mongo.update_one(proxy)
    # proxy = Proxy('218.27.136.169', port='8888')
    # mongo.delete_one(proxy)
    # for proxy in mongo.find_all():
    #     print(proxy)
    # dic = { "ip" : "218.27.136.169", "port" : "8888", "protocol" : 0, "nick_type" : 1, "speed" : 8, "score" : 50, "disable_domains" : [ 'jd.com'] }
    # dic = { "ip" : "218.27.136.168", "port" : "8888", "protocol" : 1, "nick_type" : 2, "speed" : 7, "score" : 50, "disable_domains" : [ 'taobao.com'] }
    # dic = { "ip" : "218.27.136.167", "port" : "8888", "protocol" : 0, "nick_type" : 2, "speed" : 6, "score" : 50, "disable_domains" : [ 'tianmao.com'] }
    # dic = { "ip" : "218.27.136.166", "port" : "8888", "protocol" : 1, "nick_type" : 1, "speed" : 5, "score" : 50, "disable_domains" : ['baodu.com'] }
    # dic = { "ip" : "218.27.136.165", "port" : "8888", "protocol" : 2, "nick_type" : 1, "speed" : 5, "score" : 50, "disable_domains" : ['baodu.com'] }
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)

    # for proxy in mongo.find():
    #     print(proxy)

    # for proxy in mongo.get_proxies():
    #     print(proxy)

    # mongo.disable_domain('218.27.136.165','taobao.com')

