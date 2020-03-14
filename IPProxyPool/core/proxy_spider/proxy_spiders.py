import random
import time

import requests

from core.proxy_spider.base_spider import BaseSpider

"""
1.实现西刺代理爬虫：https://www.xicidaili.com/nn/1
    定义一个类，继承通用爬虫类（BaseSpider）
    提供urls，group_xpath和detail_xpath
"""


class XiciSpider(BaseSpider):
    # 准备URL列表
    urls = ["https://www.xicidaili.com/nn/{}".format(i) for i in range(1, 11)]

    # 分组的xpath，用于获取包含代理IP的标签列表
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    # 组内xpath，用于提取ip，port，area
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()',
    }


class Ip3366Spider(BaseSpider):
    # 准备URL列表
    urls = ["http://www.ip3366.net/?stype={}&page=".format(i, j) for i in range(1, 4, 2) for j in range(1, 8)]
    # 分组的xpath，用于获取包含代理IP的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内xpath，用于提取ip，port，area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()',
    }


class KuaiSpider(BaseSpider):
    # 准备URL列表
    urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 6)]
    # 分组的xpath，用于获取包含代理IP的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内xpath，用于提取ip，port，area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }
    #当两个页面的时间间隔太短了，就报错，
    def get_page_from_url(self,url):
        time.sleep(random.uniform(1,3))
        return super().get_page_from_url(url)

# class ProxylistSpider(BaseSpider):
#     # 准备URL列表
#     urls = ["https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}".format(i) for i in range(1, 7)]
#     # 分组的xpath，用于获取包含代理IP的标签列表
#     group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
#     # 组内xpath，用于提取ip，port，area
#     detail_xpath = {
#         'ip': './td[2]/text()',
#         'port': './td[3]/text()',
#         'area': './td[5]/text()',
#     }


class IP66Spider(BaseSpider):
    # 准备URL列表
    urls = ["http://www.66ip.cn/{}.html".format(i) for i in range(1, 11)]
    # 分组的xpath，用于获取包含代理IP的标签列表
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    # 组内xpath，用于提取ip，port，area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }


if __name__ == '__main__':

    spider = IP66Spider()
    for proxy in spider.get_proxies():
        print(proxy)
