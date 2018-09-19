#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 获取代理 '

__author__ = 'fslong'

import traceback


import requests

from pool.config import *
from pool.proxyDB import ProxyDB

# 获取代理池的方法有两种，一种是通过数据库，一种是通过api接口，返回值有所不同：


def get_proxy_db():
    proxyDB = ProxyDB()
    # 获取多条请使用get_proxies函数，建议尽量多获取几条数据，因为网上找的代理经常不稳定，动不动就无法使用，虽然在自动维护代理池，但也有时效性：
    # return proxyDB.get_proxies()
    return proxyDB.get_proxy()


def get_proxy_json():
    # 获取单条数据
    params = '/proxy'
    # 获取多条数据：
    #num = input('请输入要获取的代理数量:')
    #params = '/proxies/%s/' % num
    url = 'http://127.0.0.1:'+str(API_PORT)+params
    response = requests.get(url)
    try:
        jsonData = response.json()
        return jsonData
    except:
        try:
            return response.content.decode('utf-8')
        except:
            return response.text


if __name__ == '__main__':
    print(get_proxy_db())
    print(get_proxy_json())
