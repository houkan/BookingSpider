# -*- coding: utf-8 -*-
# @Author   : Ken Hou
# @Time     : 2020-01-30 19:56
# @File     : bookinghoteldetail.py
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

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ..items import ItemBookingHoteldetailSpider

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
        sql = "SELECT * FROM hotellist where country_name = '荷兰';"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        cursor.close()
    db.close()
    return res




class BookingHoteldetailSpider(scrapy.Spider):
    name = 'bookinghoteldetail'
    allowed_domains = ['www.booking.com']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']

    start_urls = []

    url = urls()

    for item in urls():
        url = (item['hotel_url'])

        start_urls.append('https://www.booking.com' + url)

    # print(start_urls)
    #
    # print(len(start_urls))



    def parse(self, response):
        # re_selector = response.xpath(r"//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()")
        # print(re_selector)

        booking_hoteldetail_item = ItemBookingHoteldetailSpider()


        country_name = response.xpath("//div[@id='subheader-wrap']//li[2]//div[1]//a[1]/text()").extract()[0].strip()
        country_url = response.xpath("//div[@id='subheader-wrap']//li[2]//div[1]//a[1]//@href").extract()[0]
        # region_name = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]/text()").extract()[0].strip()
        # region_url = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]//@href").extract()[0]
        province_name = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]/text()").extract()[0].strip()
        province_url = response.xpath("//div[@id='subheader-wrap']//li[3]//div[1]//a[1]//@href").extract()[0]
        city_name = response.xpath("//div[@id='subheader-wrap']//li[4]//div[1]//a[1]/text()").extract()[0].strip()
        city_url = response.xpath("//div[@id='subheader-wrap']//li[4]//div[1]//a[1]//@href").extract()[0]
        type = response.xpath("//span[@class='hp__hotel-type-badge']/text()").extract()[0].strip()
        name = response.xpath("//h2[@id='hp_hotel_name']/text()").extract()[1].strip()
        url = response.xpath("//a[contains(@class,'bui_breadcrumb__link_masked')]/@href").extract()[0].strip()
        level = response.xpath("//span[@class='hp__hotel_ratings__stars nowrap']//span[1]/text()").extract()[0]
        address = response.xpath("//p[@id='showMap2']//span[2]/text()").extract()[0].strip()
        logo = response.xpath("//div[@id='photos_distinct']//a[1]/@data-photoid").extract()[0].strip()

        images = []
        image_id = 1
        try:
            while 1:
                images.append(response.xpath("//div[@id='photos_distinct']//a[" + str(image_id) + "]/@data-photoid").extract()[0].strip())
                image_id += 1
        except Exception as e:
            print('crawl', e)

        imagestr = str(images)



        # images = response.xpath("//div[@id='photos_distinct']//a[1]/@data-photoid").extract()[0].strip()
        brief = response.xpath("//div[@id='property_description_content']").extract()[0].strip()
        thumbs_up = response.xpath("//span[contains(@class,'hp__hotel_ratings')]//*[contains(@class,'-iconset-thumbs_up_square')]/@data-tooltip-follow").extract()[0].strip()
        lat = response.xpath("//a[@id='hotel_address']/@data-atlas-latlng").extract()[0].strip().split(',')[0]
        lon = response.xpath("//a[@id='hotel_address']/@data-atlas-latlng").extract()[0].strip().split(',')[1]
        comment = response.xpath("//div[contains(@class,'hp_review_score_entry')]//div[contains(@class,'bui-review-score__text')]/text()").extract()[0].strip()
        review = response.xpath("//div[contains(@class,'hp_review_score_entry')]//div[contains(@class,'bui-review-score__badge')]/text()").extract()[0].strip()


        print(imagestr)
        print(name,url,level,address)

        booking_hoteldetail_item["country_name"] = country_name
        booking_hoteldetail_item["country_url"] = country_url
        booking_hoteldetail_item["province_name"] = province_name
        booking_hoteldetail_item["province_url"] = province_url
        booking_hoteldetail_item["city_name"] = city_name
        booking_hoteldetail_item["city_url"] = city_url
        booking_hoteldetail_item["type"] = type
        booking_hoteldetail_item["name"] = name
        booking_hoteldetail_item["url"] = url
        booking_hoteldetail_item["level"] = level
        booking_hoteldetail_item["address"] = address
        booking_hoteldetail_item["logo"] = logo
        booking_hoteldetail_item["images"] = imagestr
        booking_hoteldetail_item["brief"] = brief
        booking_hoteldetail_item["thumbs_up"] = thumbs_up
        booking_hoteldetail_item["lat"] = lat
        booking_hoteldetail_item["lon"] = lon
        booking_hoteldetail_item["comment"] = comment
        booking_hoteldetail_item["review"] = review

        yield booking_hoteldetail_item


        print("酒店抓取完毕")

