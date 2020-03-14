"""
目标：把启动爬虫，启动检测代理IP，启动web服务 统一到一起
思路：
    开启三个进程，分别用于启动爬虫，检测代理IP，web服务
步骤：
    定义一个run方法用于启动代理池
        定义一个列表，用于存储要启动的进程
        创建 启动爬虫 的进程，添加到列表中
        创建 启动检测 的进程，添加到列表中
        创建 启动提供API服务 的进程，添加到列表中
        遍历进程列表，启动所有进程
    在if __name__ = '__main__';中调用run方法
"""
from multiprocessing import Process
from core.proxy_spider.run_spider import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi


def run():
    process_list = []
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyApi.start))

    for process in process_list:
        # 设置守护进程
        process.daemon = True
        process.start()

    for process in process_list:
        process.join()

if __name__ == '__main__':
    run()

