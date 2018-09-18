#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 代理池的api接口'

__author__ = 'fslong'

import asyncio

import pymongo
import json
from aiohttp import web

from pool.proxyDB import ProxyDB
from pool.config import *


class Api(object):
    async def index(self, request):
        # await asyncio.sleep(0.5)
        text = '<h2>Welcome to Proxy Pool System</h2>'
        return web.Response(text=text, content_type='text/html')

    async def proxy(self, request):
        proxyDB = ProxyDB()
        try:
            _proxy = proxyDB.get_proxy()
            result = {'ip': _proxy['ip'], 'port': _proxy['port']}
            text = json.dumps(result)
            return web.Response(text=text, content_type='application/json')
        except:
            result = proxyDB.get_proxy()
            return web.Response(text=str(result), content_type='text/html')

    async def proxies(self, request):
        proxyDB = ProxyDB()
        try:
            num = int(request.match_info['num'])
        except:
            num = 10
        try:
            result = []
            _proxies = proxyDB.get_proxies(num=num)
            for _proxy in _proxies:
                result.append({'ip': _proxy['ip'], 'port': _proxy['port']})
            text = json.dumps(result)
            return web.Response(text=text, content_type='application/json')
        except:
            result = proxyDB.get_proxies(num=num)
            return web.Response(text=result, content_type='text/html')

    async def init(self, loop):
        app = web.Application()
        app.router.add_route('GET', '/', self.index)
        app.router.add_route('GET', '/proxy', self.proxy)
        app.router.add_route('GET', '/proxies/{num}/', self.proxies)
        app.router.add_route('GET', '/proxies/', self.proxies)
        srv = await loop.create_server(app._make_handler(), '127.0.0.1', API_PORT)
        print('Server started at http://127.0.0.1:%s...' % API_PORT)
        return srv

    def service(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init(loop))
        loop.run_forever()


if __name__ == '__main__':
    api = Api()
    api.service()
