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
                print('%s未能保存成功！' % (proxy))

        print('\033[1;35m%s\033[0m个代理存入数据库成功！' % len(proxies))

    def get_all_id(self):
        try:
            allProxiesId = []
            for proxy in self.collection.find():
                allProxiesId.append(proxy['id'])
            return allProxiesId
        except:
            return False

    def get_proxies_num(self):
        try:
            return self.collection.count_documents({})
        except:
            return False

    def get_proxy(self):
        allProxiesId = self.get_all_id()
        if allProxiesId:
            proxyId = random.randint(0, len(allProxiesId)-1)
            try:
                return self.collection.find_one({'id': allProxiesId[proxyId]})
            except:
                return False
        else:
            return False

    def get_proxies(self, num=MIN_PROXIES_NUM):
        proxies = []
        proxiesId = []
        allProxiesId = self.get_all_id()
        if allProxiesId:
            while len(proxiesId) < num:
                proxyId = random.randint(0, self.get_proxies_num()-1)
                if not allProxiesId[proxyId] in proxiesId:
                    proxiesId.append(allProxiesId[proxyId])
            try:
                for proxy in self.collection.find({'id': {'$in': proxiesId}}):
                    proxies.append(proxy)
                return proxies
            except:
                return False
        else:
            return False

    def get_all_proxies(self):
        allProxies = []
        try:
            for proxy in self.collection.find():
                allProxies.append(proxy)
            return allProxies
        except:
            return False

    def del_proxy(self, proxyId, count=1):
        if count >= 5:
            print('多次尝试删除，均失败，请检查相关代码！')
            return False
        try:
            self.collection.delete_one({'id': proxyId})
        except:
            print('id=%s的代理删除失败，开始重试...' % proxyId)
            count += 1
            self.del_proxy(proxyId, count=count)

    def del_all_proxies(self, count=1):
        if count >= 5:
            print('多次尝试删除，均失败，请检查相关代码！')
            return False
        all_id = self.get_all_id()
        if all_id:
            try:
                self.collection.delete_many({'id': {'$in': self.get_all_id()}})
            except:
                count += 1
                self.del_all_proxies(count=count)


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
