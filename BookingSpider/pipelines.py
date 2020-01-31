# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json

import pymysql
import pymysql.cursors

from twisted.enterprise import adbapi
from twisted.internet import reactor


# class MysqlTwistedPipeline(object):
#     def process_item(self, item, spider):
#         return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('booking.json','w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()








# Twisted只是提供一个异步容器，本身没提供数据库链接


# 导入洲的表格
class ContinentMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into continent(continent_id,continent_name)
                    VALUES (%s,%s)
                    """
        cursor.execute(insert_sql, (item['continent_id'], item['continent_name']))




# 导入国家的表格
class CountryMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into country(continent_id,continent_name,country_id,country_name,country_url)
                    VALUES (%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (item['country_continent_id'], item['country_continent_name'], item['country_general_id'], item['country_name'], item['country_url']))




# 导入城市的表格
class CityMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)


    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into city(city_id,city_name,city_url)
                    VALUES (%s,%s,%s)
                    """
        cursor.execute(insert_sql, (item['city_general_id'], item['city_name'], item['city_url']))




# 导入酒店的表格
class HotelMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)


    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into hotel(hotel_id,hotel_name,hotel_url,hotel_level,country_name,country_url,province_name,province_url,city_name,city_url)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (item['hotel_general_id'], item['hotel_name'], item['hotel_url'], item['hotel_level'], item['country_name'], item['country_url'], item['province_name'], item['province_url'], item['city_name'], item['city_url']))




# 导入酒店详细信息的表格
class HoteldetailMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)


    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into hoteldetail(
                    country_name,
                    country_url,
                    province_name,
                    province_url,
                    city_name,
                    city_url,
                    type,
                    name,
                    url,
                    level,
                    address,
                    logo,
                    images,
                    brief,
                    thumbs_up,
                    lat,
                    lon,
                    comment,
                    review
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (
            item['country_name'],
            item['country_url'],
            item['province_name'],
            item['province_url'],
            item['city_name'],
            item['city_url'],
            item['type'],
            item['name'],
            item['url'],
            item['level'],
            item['address'],
            item['logo'],
            item['images'],
            item['brief'],
            item['thumbs_up'],
            item['lat'],
            item['lon'],
            item['comment'],
            item['review']
        ))





# 导入酒店详细信息的表格
class HoteldetailjsMysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USERNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert,item)
        #错误处理
        query.addErrback(self.handle_error)

    #错误处理函数
    def handle_error(self,falure):
        print(falure)


    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into hoteldetailjs(
                    country_name,
                    country_url,
                    province_name,
                    province_url,
                    city_name,
                    city_url,
                    type,
                    name,
                    url,
                    level,
                    address,
                    logo,
                    images,
                    brief,
                    thumbs_up,
                    lat,
                    lon,
                    comment,
                    review
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (
            item['country_name'],
            item['country_url'],
            item['province_name'],
            item['province_url'],
            item['city_name'],
            item['city_url'],
            item['type'],
            item['name'],
            item['url'],
            item['level'],
            item['address'],
            item['logo'],
            item['images'],
            item['brief'],
            item['thumbs_up'],
            item['lat'],
            item['lon'],
            item['comment'],
            item['review']
        ))

