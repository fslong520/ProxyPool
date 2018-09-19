#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 代理池对数据库的相关操作 '

__author__ = 'fslong'
import pymongo
import traceback
from pool.config import *
import random
from pymongo.errors import CollectionInvalid, ConnectionFailure, ExecutionTimeout


class ProxyDB(object):
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                host=MONGO_HOST, port=MONGO_PORT)
            self.db = self.client[MONGO_DB]
            self.collection = self.db['ip代理']
        except (CollectionInvalid, ConnectionFailure) as s:
            print(s)
        except:
            traceback.print_exc()

    def save_proxies_to_mongodb(self, proxies):
        count = 0
        for proxy in proxies:
            count += 1
            data = dict()
            data['id'] = count
            data['ip'] = proxy.split(':')[0]
            data['port'] = proxy.split(':')[1]
            try:
                self.collection.insert_one(data)
            except:
                traceback.print_exc()
                return False

        print('\033[1;35m%s\033[0m个代理存入数据库成功！' % len(proxies))

    def get_all_id(self):
        allProxiesId = []
        for proxy in self.collection.find():
            allProxiesId.append(proxy['id'])
        return allProxiesId

    def get_proxies_num(self):
        return self.collection.count_documents({})

    def get_proxy(self):
        allProxiesId = self.get_all_id()
        proxyId = random.randint(0, len(allProxiesId)-1)
        return self.collection.find_one({'id': allProxiesId[proxyId]})

    def get_proxies(self, num=10):
        proxies = []
        proxiesId = []
        allProxiesId = self.get_all_id()
        while len(proxiesId) < num:
            proxyId = random.randint(0, self.get_proxies_num()-1)
            if not allProxiesId[proxyId] in proxiesId:
                proxiesId.append(allProxiesId[proxyId])
        for proxy in self.collection.find({'id': {'$in': proxiesId}}):
            proxies.append(proxy)
        return proxies

    def get_all_proxies(self):
        allProxies = []
        for proxy in self.collection.find():
            allProxies.append(proxy)
        return allProxies

    def del_proxy(self, proxyId):
        self.collection.delete_one({'id': proxyId})

    def del_all_proxies(self):
        self.collection.delete_many({'id': {'$in': self.get_all_id()}})


if __name__ == '__main__':
    proxyDB = ProxyDB()
    '''
    proxyDB.save_proxies_to_mongodb(['172.16.1.2:9900', '172.16.1.2:9901''172.16.1.2:9900', '172.16.1.2:9901',
                                     '172.16.1.2:9900', '172.16.1.2:9901', '172.16.1.2:9900', '172.16.1.2:9901', '172.16.1.2:9900', '172.16.1.2:9901'])
    '''
    # proxyDB.del_all_proxies()
    print(proxyDB.get_proxies_num())
    print(proxyDB.get_proxy())
    proxyDB.del_proxy(2)
    print(proxyDB.get_proxies(3))
    print(proxyDB.get_all_proxies())
