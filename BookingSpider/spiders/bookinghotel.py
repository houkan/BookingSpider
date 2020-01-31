# -*- coding: utf-8 -*-
# @Author   : Ken Hou
# @Time     : 2020-01-30 10:29
# @File     : bookinghotel.py
# @Software : PyCharm
# @Project  : BookingSpider
# @User     : kan
# ----------------------------

# -*- coding: utf-8 -*-
import scrapy
import re


import pymysql
import pymysql.cursors

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ..items import ItemBookingHotelSpider

def urls():

    config={
        "host":"localhost",
        "user":"booking",
        "password":"booking",
        "database":"booking",
        "charset":"utf8"
    }
    db = pymysql.connect(**config)
    with db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:  #获取数据库连接的对象
        sql = "SELECT * FROM city_full where continent_id = 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        cursor.close()
    db.close()
    return res



class BookingHotelSpider(scrapy.Spider):
    name = 'bookinghotel'
    allowed_domains = ['www.booking.com']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']

    start_urls = []

    url = urls()

    for item in urls():
        url = (item['url'])

        start_urls.append('https://www.booking.com' + url)

    print(start_urls)

    print(len(start_urls))



    def parse(self, response):
        # re_selector = response.xpath(r"//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()")
        # print(re_selector)

        booking_hotel_item = ItemBookingHotelSpider()

        order_id = 1

        try:

            while 1:

                country_name = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]/text()").extract()[0].strip()
                country_url = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]//@href").extract()[0]
                province_name = response.xpath("//div[@id='subheader-wrap']//li[4]//div[1]//a[1]/text()").extract()[0].strip()
                province_url = response.xpath("//div[@id='subheader-wrap']//li[4]//div[1]//a[1]//@href").extract()[0]
                city_name = response.xpath("//div[@class='dest-sitemap__landing']//a/text()").extract()[0].strip()
                city_url = response.xpath("//div[@class='dest-sitemap__landing']//a//@href").extract()[0]

                # city_name = response.xpath("//li[2]//h3[1]/text()").extract()[0].strip()
                hotel_level = response.xpath("(//div[4]/div[2]/ul[1]/li[2]/ul[1]/li["+ str(order_id) + "]/h4[1]/text())").extract()[0].strip()

                order_name = response.xpath("(//div[4]/div[2]/ul[1]/li[2]/ul[1]/li["+ str(order_id) + "]/h4[1]/text())").extract()[0].strip()
                print(order_id, order_name)

                hotel_id = 1

                try:
                    while 1:
                        # country = response.xpath("//li[@class='dest-sitemap__list-item']//li[2]//div[1]//ul[1]//li[2]//a[1]").extract()[0].strip()
                        hotel_general_id = hotel_id + order_id * 10000

                        # hotel_name = response.xpath("//div[2]/ul[1]/li[2]/ul[1]/li[" + str(order_id) + "]/div[1]/ul[1]/li[" + str(hotel_id) + "]/a[1]/text()").extract()[0].strip()
                        # hotel_url = response.xpath("//div[2]/ul[1]/li[2]/ul[1]/li[" + str(order_id) + "]/div[1]/ul[1]/li[" + str(hotel_id) + "]//a[1]//@href").extract()[0]
                        hotel_name = response.xpath("//div[4]/div[2]/ul[1]/li[2]/ul[1]/li[" + str(order_id) + "]/div[1]/ul[1]/li[" + str(hotel_id) + "]/a[1]/text()").extract()[0].strip()
                        hotel_url = response.xpath("//div[4]/div[2]/ul[1]/li[2]/ul[1]/li[" + str(order_id) + "]/div[1]/ul[1]/li[" + str(hotel_id) + "]//a[1]//@href").extract()[0]

                        print(order_id, order_name, hotel_general_id, hotel_name, hotel_url)

                        # booking_city_item["continent_id"] = continent_id
                        # booking_city_item["continent_name"] = continent_name
                        # booking_city_item["country_general_id"] = country_general_id
                        # booking_city_item["country_name"] = country_name
                        # booking_city_item["country_url"] = country_url
                        booking_hotel_item["country_name"] = country_name
                        booking_hotel_item["country_url"] = country_url
                        booking_hotel_item["province_name"] = province_name
                        booking_hotel_item["province_url"] = province_url
                        booking_hotel_item["city_name"] = city_name
                        booking_hotel_item["city_url"] = city_url
                        booking_hotel_item["hotel_level"] = hotel_level
                        booking_hotel_item["hotel_general_id"] = hotel_general_id
                        booking_hotel_item["hotel_name"] = hotel_name
                        booking_hotel_item["hotel_url"] = hotel_url
                        yield booking_hotel_item

                        print(hotel_name + "酒店抓取完毕")
                        hotel_id += 1

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

            print("城市抓取完毕")

