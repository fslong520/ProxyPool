#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 获取页面的模块 '

__author__ = 'fslong'
import random

import requests
from fake_useragent import FakeUserAgentError, UserAgent
from requests.exceptions import ConnectionError

from pool.config import *


def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    }
    headers = dict(base_headers, **options)
    print('开始获取\033[1;34m %s \033[0m的数据...' % url)
    try:
        r = requests.get(url, headers=headers, timeout=GET_TIMEOUT)
        if r.status_code == 200:
            print('成功获取\033[1;34m %s \033[0m的数据\033[1;35m%s OK\033[0m开始解析...' % (
                url, r.status_code))
            try:
                return r.content.decode('utf-8')
            except:
                return r.text

    except ConnectionError:
        print('\033[1;31m %s \033[0m的数据获取失败，请重试...' % url)
        return False
