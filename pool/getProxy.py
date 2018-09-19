#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 获取代理的模块 '

__author__ = 'fslong'

import asyncio

import pyquery

from pool.checkProxy import checkProxy
from pool.getPage import get_page
from pool.config import *
from pool.proxyDB import ProxyDB


class GetProxy(object):
    def __init__(self):
        self.PROXY_COUNT = 0
        self.proxies = []

    # 检查爬取到的数据是否足够:

    def check_count(self):
        if self.PROXY_COUNT > MAX_PROXIES_NUM:
            print('爬取的代理数量已经足够，暂停爬取。')
            self.proxies = self.proxies[0-MAX_PROXIES_NUM:]
            return False
        else:
            return True

    async def __check_proxy(self, proxy):
        # 直接连续测试两次，都成功的才会添加到数据库：
        # 并且判断是否已经存在该数据了：
        if not proxy in self.proxies:
            if await checkProxy(proxy):
                self.proxies.append(proxy)
                self.PROXY_COUNT += 1
                print(
                    '目前已获取到可用的代理数为：\033[1;32m%s\033[0m' % self.PROXY_COUNT)
        else:
            print('代理\033[1;34m %s \033[0m已经在数据库当中了...' % proxy)

    def get_proxies(self):
        self.get_from_66ip()
        self.get_from_kuaidaili()
        self.get_from_yqie()
        proxyDB = ProxyDB()
        proxyDB.del_all_proxies()
        try:
            proxyDB.save_proxies_to_mongodb(self.proxies)
        except:
            pass

    def get_from_kuaidaili(self):
        proxies = []
        base_url = 'https://www.kuaidaili.com/free/intr/{}/'  # 透明代理
        # base_url = 'https://www.kuaidaili.com/free/inha/{}/'  # 高匿代理
        page = 0
        while self.PROXY_COUNT < MAX_PROXIES_NUM and page < 50:
            page += 1
            url = base_url.format(page)
            html = get_page(url)
            if html:
                pq = pyquery.PyQuery(html)
                for item in pq('.table > tbody > tr').items():
                    proxy = item('td:nth-child(1)').text() + \
                        ':'+item('td:nth-child(2)').text()
                    # 替换掉空格
                    proxy = proxy.replace(' ', '')
                    proxies.append(proxy)
                print('数据解析成功，开始测试代理有效性...')
                if not proxies == []:
                    loop = asyncio.get_event_loop()
                    tasks = [self.__check_proxy(proxy) for proxy in proxies]
                    loop.run_until_complete(asyncio.wait(tasks))
        self.check_count()

    def get_from_66ip(self):
        proxies = []
        base_url = 'http://www.66ip.cn/{}.html'  # 多数是高匿代理
        page = 0
        while self.PROXY_COUNT < MAX_PROXIES_NUM and page < 50:
            page += 1
            url = base_url.format(page)
            html = get_page(url)
            if html:
                pq = pyquery.PyQuery(html)
                for item in pq('.container table tr').items():
                    if 'ip' in item.text():
                        pass
                    else:
                        proxy = item('td:nth-child(1)').text() + \
                            ':'+item('td:nth-child(2)').text()
                        # 替换掉空格
                        proxy = proxy.replace(' ', '')
                        proxies.append(proxy)
                print('数据解析成功，开始测试代理有效性...')
                if not proxies == []:
                    loop = asyncio.get_event_loop()
                    tasks = [self.__check_proxy(proxy) for proxy in proxies]
                    loop.run_until_complete(asyncio.wait(tasks))
        self.check_count()

    def get_from_yqie(self):
        proxies = []
        url = 'http://ip.yqie.com/ipproxy.htm'
        if self.PROXY_COUNT < MAX_PROXIES_NUM:
            html = get_page(url)
            if html:
                pq = pyquery.PyQuery(html)
                for table in pq('table').items():
                    for item in table('tr').items():
                        if '端口' in item.text():
                            pass
                        else:
                            proxy = item('td:nth-child(1)').text() + \
                                ':'+item('td:nth-child(2)').text()
                            # 替换掉空格
                            proxy = proxy.replace(' ', '')
                            proxies.append(proxy)
                print('数据解析成功，开始测试代理有效性...')
                if not proxies == []:
                    loop = asyncio.get_event_loop()
                    tasks = [self.__check_proxy(proxy) for proxy in proxies]
                    loop.run_until_complete(asyncio.wait(tasks))
        self.check_count()


if __name__ == '__main__':
    getProxy = GetProxy()
    getProxy.get_proxies()
    # print(getProxy.proxies)
