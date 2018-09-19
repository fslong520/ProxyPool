#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 代理池的主程序，执行本程序即可启动代理池。 '

__author__ = 'fslong'

import asyncio
import os
import time
from multiprocessing import Process

from pool.api import Api
from pool.checkProxy import checkProxy
from pool.config import *
from pool.getProxy import GetProxy
from pool.proxyDB import ProxyDB


class Service(object):
    def __init__(self):
        self.proxyDB = ProxyDB()

    def check_proxies_num(self):
        proxiesNum = self.proxyDB.get_proxies_num()
        if proxiesNum < MIN_PROXIES_NUM:
            print(
                '\033[1;31m由于可用代理数量已经低于设定的代理池最小数量:%s，将会重新抓取并重建数据库...\033[0m' % MIN_PROXIES_NUM)
            getProxy = GetProxy()
            getProxy.get_proxies()

    async def __check_proxy(self, proxy):
        if not await checkProxy(proxy['ip']+':'+proxy['port']):
            # 首次检测无效之后进行第二次检测，如果依然无效就删库跑路:
            if not await checkProxy(proxy['ip']+':'+proxy['port'], count=2):
                if not await checkProxy(proxy['ip']+':'+proxy['port'], count=3):
                    self.proxyDB.del_proxy(proxy['id'])

    def check_proxies_istrue(self):
        print(
            '\033[1;32m\n-------------------------------\n开始检测代理池中代理的有效性...\n-------------------------------\n\033[0m')
        proxies = self.proxyDB.get_all_proxies()
        if not proxies == []:
            loop = asyncio.get_event_loop()
            tasks = [self.__check_proxy(proxy) for proxy in proxies]
            loop.run_until_complete(asyncio.wait(tasks))
            print('还剩下\033[1;35m%s\033[0m个可用代理，\033[1;32m%s\033[0m秒后将会重新检测...' %
                  (self.proxyDB.get_proxies_num(), CHECK_TIMEDELAY))
        self.check_proxies_num()
        time.sleep(CHECK_TIMEDELAY)


def main():

    def api_service():
        api = Api()
        api.service()

    def proxy_pool_service():
        service = Service()
        while True:
            service.check_proxies_istrue()
    p1 = Process(target=api_service, args=())
    p2 = Process(target=proxy_pool_service, args=())
    p1.start()
    # p1.join()
    p2.start()
    # p2.join()


if __name__ == '__main__':
    main()
