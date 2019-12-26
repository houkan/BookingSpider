# -*- coding: utf-8 -*-
import scrapy
import re


import pymysql
import pymysql.cursors

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ..items import ItemBookingCitySpider

def urls():

    config={
        "host":"localhost",
        "user":"root",
        "password":"root",
        "database":"booking",
        "charset":"utf8"
    }
    db = pymysql.connect(**config)
    with db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:  #获取数据库连接的对象
        sql = "SELECT * FROM country where continent_id = 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        cursor.close()
    db.close()
    return res



class BookingCitySpider(scrapy.Spider):
    name = 'bookingcity'
    allowed_domains = ['www.booking.com']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']

    start_urls = []

    url = urls()

    for item in urls():
        url = (item['country_url'])

        start_urls.append('https://www.booking.com' + url)

    print(start_urls)

    print(len(start_urls))



    def parse(self, response):
        # re_selector = response.xpath(r"//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()")
        # print(re_selector)

        booking_city_item = ItemBookingCitySpider()

        order_id = 1

        try:

            while 1:

                order_name = response.xpath("//li[@class='dest-sitemap__list-item']//li["+ str(order_id) + "]//h4[1]/text()").extract()[0].strip()
                print(order_id, order_name)

                city_id = 1

                try:
                    while 1:
                        # country = response.xpath("//li[@class='dest-sitemap__list-item']//li[2]//div[1]//ul[1]//li[2]//a[1]").extract()[0].strip()
                        city_general_id = city_id + order_id * 10000

                        city_name = response.xpath("//li[@class='dest-sitemap__list-item']//li[" + str(order_id) + "]//div[1]//ul[1]//li[" + str(city_id) + "]//a[1]/text()").extract()[0].strip()
                        city_url = response.xpath("//li[@class='dest-sitemap__list-item']//li[" + str(order_id) + "]//div[1]//ul[1]//li[" + str(city_id) + "]//a[1]//@href").extract()[0]

                        print(order_id, order_name, city_general_id, city_name, city_url)

                        # booking_city_item["continent_id"] = continent_id
                        # booking_city_item["continent_name"] = continent_name
                        # booking_city_item["country_general_id"] = country_general_id
                        # booking_city_item["country_name"] = country_name
                        # booking_city_item["country_url"] = country_url
                        booking_city_item["city_general_id"] = city_general_id
                        booking_city_item["city_name"] = city_name
                        booking_city_item["city_url"] = city_url
                        yield booking_city_item

                        print(city_name + "城市分析完毕")
                        city_id += 1

                except Exception as e:
                        print('crawl', e)

                order_id += 1

                # continent = response.xpath("//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()").extract()[0].strip()
                # print(continent)
                # continent_selector = response.xpath("//li[1]//h4[1]/text()")
                # continent = continent_selector.extract()
                # continent_clean =  [x.strip() for x in continent if x.strip() != '']
                # print(continent_clean)


        except Exception as e:
            print('crawl', e)

            print("国家分析完毕")

