"""
目标：实现可以指定不同url列表，分组的XPATH和详情的XPATH，从不同页面上提取代理的IP，
端口号和区域的通用爬虫
步骤：
1.在base_spider.py文件中，定义一个BaseSpider类，继承Object
2.提供三个类成员变量：
    urls：代理IP网址的URL的列表
    group_xpath：分组XPATH，获取包含代理IP信息标签列表的XPATH
    detail_xpath：组内xpath，获取代理IP详情的信息xpath，格式：{'ip':'xx','port':'xx','area':'xx'}
3.提供初始化的方法，传入爬虫URL列表，分组xpath，详情（组内）xpath
4.对外提供一个获取代理ip的方法
    4.1遍历url列表，获取url
    4.2根据发送请求，获取页面数据
    4.3解析页面，提取数据，封装proxy对象
    4.4返回proxy对象列表
"""
from lxml import etree

import requests

from domain import Proxy
from utils.http import get_request_headers
from utils.log import logger


class BaseSpider(object):
    urls = []

    group_xpath = ''

    detail_xpath = {}

    def __init__(self,urls=[],group_xpath='',detail_xpath={}):

        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath


    def get_page_from_url(self,url):
        headers = get_request_headers()
        """根据url发送请求，获取页面数据"""
        response = requests.get(url,headers=headers)
        return response.content

    def get_first_from_list(self,lis):
        return lis[0] if len(lis) != 0 else ''


    def get_proxies_from_page(self,page):
        """解析页面，提取数据，封装为Proxy对象"""
        element = etree.HTML(page)
        # 获取包含代理IP信息的标签信息
        trs = element.xpath(self.group_xpath)
        #遍历trs，获取代理IP相关信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip,port,area=area)
            # 使用yield返回对象列表
            yield proxy

    def get_proxies(self):
        #4. 对外提供一个获取代理IP的方法
        #4.1 遍历url列表，获取url
        for url in self.urls:
            #4.2 根据发送请求，获取页面数据
            page = self.get_page_from_url(url)

            #4.3 解析页面，提取数据，封装给为Proxy对象
            proxies = self.get_proxies_from_page(page)

            yield from proxies


if __name__ == '__main__':

    config = {
        'urls':['http://www.ip3366.net/?stype=1&page={}'.format(i) for i in range(1,4)],
        'group_xpath':'//*[@id="list"]/table/tbody/tr',
        'detail_xpath':{
            'ip':'./td[1]/text()',
            'port':'./td[2]/text()',
            'area':'./td[6]/text()',
        }
    }

    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)

