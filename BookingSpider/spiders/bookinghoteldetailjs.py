# -*- coding: utf-8 -*-
# @Author   : Ken Hou
# @Time     : 2020-01-31 16:32
# @File     : bookinghoteldetailjs.py
# @Software : PyCharm
# @Project  : BookingSpider
# @User     : kan
# ----------------------------



# -*- coding: utf-8 -*-
import scrapy
import re


import pymysql
import pymysql.cursors
import json
import js2xml

import sys,os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append("../")

# from lxml import etree
from lxml import html
etree = html.etree

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from BookingSpider.items import ItemBookingHoteldetailjsSpider

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
        sql = "SELECT * FROM hotel_full where country_url = '/country/at.html' and concat('https://www.booking.com',hotel_url) not in(select url from hoteldetailjs);"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        cursor.close()
    db.close()
    return res




class BookingHoteldetailjsSpider(scrapy.Spider):
    name = 'bookinghoteldetailjs'
    allowed_domains = ['www.booking.com']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']
    # start_urls = []

    redis_key = "bookinghoteldetailjs:start_urls"




    # url = urls()
    #
    # for item in urls():
    #     url = (item['hotel_url'])
    #
    #     start_urls.append('https://www.booking.com' + url)

    # print(start_urls)

    # print(len(start_urls))



    def parse(self, response):
        # re_selector = response.xpath(r"//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()")
        # print(re_selector)

        booking_hoteldetailjs_item = ItemBookingHoteldetailjsSpider()

        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

        jsdata = response.xpath('/html[1]/body[1]/script[1]/text()').extract_first()
        xmldata = js2xml.pretty_print(js2xml.parse(jsdata, encoding='utf-8', debug=False))
        selector = etree.HTML(xmldata)



        # country_name = data["address"]["addressCountry"]
        country_url = ""
        # region_name = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]/text()").extract()[0].strip()
        # region_url = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]//@href").extract()[0]
        province_name = ""
        province_url = ""
        # city_name = ""
        city_url = ""
        # type = data["@type"]
        # name = data["name"]
        url = data["url"]
        # level = ""
        address = data["address"]["streetAddress"]
        logo = data["image"]

        hotel_id = selector.xpath('//property[@name="hotel_id"]/string/text()')[0]
        name = selector.xpath('//property[@name="hotel_name"]/string/text()')[0]

        try:
            level = selector.xpath('//property[@name="hotel_class"]/number/@value')[0]
        except Exception as e:
            level = ""
            print('crawl', e)

        city_id = selector.xpath('//property[@name="dest_ufi"]/string/text()')[0]
        type = selector.xpath('//property[@name="dest_type"]/string/text()')[0]
        city_name = selector.xpath('//property[@name="city_name"]/string/text()')[0]
        dest_name = selector.xpath('//property[@name="dest_name"]/string/text()')[0]
        region_name = selector.xpath('//property[@name="region_name"]/string/text()')[0]
        country_name = selector.xpath('//property[@name="country_name"]/string/text()')[0]
        category = selector.xpath('//property[@name="atnm"]/string/text()')[0]

        images = []
        image_id = 1
        try:
            while 1:
                images.append(response.xpath("//div[@id='photos_distinct']//a[" + str(image_id) + "]/@data-photoid").extract()[0].strip())
                image_id += 1
        except Exception as e:
            print('crawl', e)

        imagestr = str(images)



        # images = data["image"]
        brief = data["description"]
        thumbs_up = ""
        lat = data["hasMap"].split('center=')[1].split('&')[0].split(',')[0]
        lon = data["hasMap"].split('center=')[1].split('&')[0].split(',')[1]

        try:
            comment = data["aggregateRating"]["reviewCount"]
        except Exception as e:
            comment = ""
            print('crawl', e)

        try:
            review = data["aggregateRating"]["ratingValue"]
        except Exception as e:
            review = ""
            print('crawl', e)



        # print(imagestr)
        print(name,url,level,address)

        booking_hoteldetailjs_item["country_name"] = country_name
        booking_hoteldetailjs_item["country_url"] = country_url
        booking_hoteldetailjs_item["province_name"] = province_name
        booking_hoteldetailjs_item["province_url"] = province_url
        booking_hoteldetailjs_item["city_name"] = city_name
        booking_hoteldetailjs_item["city_url"] = city_url
        booking_hoteldetailjs_item["type"] = type
        booking_hoteldetailjs_item["name"] = name
        booking_hoteldetailjs_item["url"] = url
        booking_hoteldetailjs_item["level"] = level
        booking_hoteldetailjs_item["address"] = address
        booking_hoteldetailjs_item["logo"] = logo
        booking_hoteldetailjs_item["images"] = imagestr
        booking_hoteldetailjs_item["brief"] = brief
        booking_hoteldetailjs_item["thumbs_up"] = thumbs_up
        booking_hoteldetailjs_item["lat"] = lat
        booking_hoteldetailjs_item["lon"] = lon
        booking_hoteldetailjs_item["comment"] = comment
        booking_hoteldetailjs_item["review"] = review
        booking_hoteldetailjs_item["hotel_id"] = hotel_id
        booking_hoteldetailjs_item["city_id"] = city_id
        booking_hoteldetailjs_item["dest_name"] = dest_name
        booking_hoteldetailjs_item["region_name"] = region_name
        booking_hoteldetailjs_item["category"] = category


        yield booking_hoteldetailjs_item


        print("酒店抓取完毕")

