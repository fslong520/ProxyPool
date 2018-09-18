#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 代理池对数据库的相关操作 '

__author__ = 'fslong'
import pymongo
from config import *
import random


class ProxyDB(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db['ip代理']

    def save_proxies_to_mongodb(self, proxies):
        count = 0
        for proxy in proxies:
            count += 1
            data = dict()
            data['id'] = count
            data['ip'] = proxy.split(':')[0]
            data['port'] = proxy.split(':')[1]
            self.collection.insert_one(data)

    def get_proxies_num(self):
        return self.collection.count_documents({})

    def get_proxy(self):
        proxyId = random.randint(1, self.get_proxies_num())
        return self.collection.find_one({'id': proxyId})


if __name__ == '__main__':
    proxyDB = ProxyDB()
    #proxyDB.save_proxies_to_mongodb(['172.16.1.2:9900', '172.16.1.2:9901'])
    print(proxyDB.get_proxies_num())
    print(proxyDB.get_proxy())
