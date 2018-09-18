#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 检查代理是否有效的模块 '

__author__ = 'fslong'

import asyncio
import traceback

import aiohttp
from fake_useragent import FakeUserAgentError, UserAgent

from pool.config import *

try:
    from asyncio import TimeoutError
    from aiohttp.errors import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError


async def checkProxy(proxy, options={}):
    if not proxy.startswith('http'):
        print('检测\033[1;34m %s \033[0m的有效性...' % proxy)
        url = 'http://'+proxy
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(TEST_API, proxy=url, timeout=CHECK_TIMEOUT) as response:
                        if response.status == 200:
                            print(
                                '代理\033[1;34m %s \033[0m\033[1;32m测试通过...\033[0m' % proxy)
                            return True
                except (ProxyConnectionError, TimeoutError, ValueError):
                    # traceback.print_exc()
                    print(
                        '代理\033[1;34m %s \033[0m\033[1;31m测试无效\033[0m...' % proxy)
                    return False

        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            # print(s)
            print(
                '代理\033[1;34m %s \033[0m\033[1;31m测试无效\033[0m...' % proxy)
            return False
        except:
            # traceback.print_exc()
            print(
                '代理\033[1;34m %s \033[0m\033[1;31m测试无效\033[0m...' % proxy)
            return False
