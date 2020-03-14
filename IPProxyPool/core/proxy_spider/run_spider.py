
"""
目标：根据配置文件信息，加载爬虫，抓取代理IP，如果可用，写入到数据库中
思路：
    在run_spiders.py中，创建RunSpiser类
    提供一个运行爬虫的run方法，作为运行爬虫的入口，实现核心处理逻辑
        根据配置文件信息，获取爬虫对象列表
        遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理iP
        监测代理类IP代理（数据库模型）
        如果可用，写入数据库
        处理异常，防止一个爬虫内部出错，影响其他的爬虫
    使用异步来执行任务，以提高抓取代理IP的效率
        在init方法中创建协程池对象
        把处理一个代理爬虫的代码抽到一个方法
        使用异步执行这个方法
        调用协程的join方法，让当前线程等待队列完成
    使用schedule模块，实现每隔一定时间，执行一次爬取任务
        定义一个start的类方法
        创建当前类的对象，调用run方法
        使用schedule模块，每隔一定的时间，执行当前对象的run方法
"""
import time


#打猴子补丁
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

from settings import PROXIES_SPIDERS,RUN_SPIDERS_INTERVAL
import importlib
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger

import schedule

class RunSpider(object):

    def __init__(self):
        #创建MongoDB对象
        self.mongo_pool = MongoPool()
        #在init中创建协程池
        self.coroutine_pool = Pool()

    def get_spider_from_setting(self):
        """根据配置文件信息，获取爬虫对象列表"""
        #遍历配置文件中爬虫信息，获取每隔爬虫的全类名
        for full_class_name in PROXIES_SPIDERS:
            #获取模块名和类名
            module_name,class_name = full_class_name.rsplit('.', maxsplit=1)
            #根据模块名导入模块
            module = importlib.import_module(module_name)
            #根据类名，从模块中获取类
            cls = getattr(module,class_name)
            #创建爬虫对象
            spider = cls()

            yield spider

    def run(self):
        #2.1根据配置文件信息，获取爬虫对象列表
        spiders = self.get_spider_from_setting()
        for spider in spiders:
            #2.5处理异常，防止一个爬虫内部出错，影响其他的爬虫
            #3.3 通过异步执行这个方法
            self.coroutine_pool.apply_async(self.__execute_one_spider_tack,args=(spider,))
        # 调用协程的join方法，让当前线程等待队列完成
        self.coroutine_pool.join()


    def __execute_one_spider_tack(self, spider):
        #3.2 把处理一个代理爬虫的代码抽到一个方法
        #用于处理一个爬虫任务
        try:
            # 遍历爬虫对象的get_proxies方法，获取代理IP
            for proxy in spider.get_proxies():
                # 监测代理IP
                proxy = check_proxy(proxy)
                # 2.4如果可用，写入数据库
                # 如果spider不为-1，说明可用
                if proxy.speed != -1:
                    # 写入数据库
                    self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        """
        使用schedule模块，实现每隔一定时间，执行一次爬取任务
        定义一个start的类方法
        创建当前类的对象，调用run方法
        使用schedule模块，每隔一定的时间，执行当前对象的run方法

        :return:
        """
        rs = RunSpider()
        rs.run()
        schedule.every(RUN_SPIDERS_INTERVAL).hour.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(1)



if __name__ == '__main__':
    # rs = RunSpider()
    # rs.run()
    RunSpider.start()
    #测试schedule
    # def task():
    #     print('aa')
    #
    # schedule.every(2).seconds.do(task)
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(1)


















