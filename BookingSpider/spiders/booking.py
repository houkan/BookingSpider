# -*- coding: utf-8 -*-
import scrapy
import re


import pymysql
import pymysql.cursors

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ..items import ItemBookingContinentSpider
from ..items import ItemBookingCountrySpider


class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/destination.zh-cn.html']
    # start_urls = ['https://www.booking.com/destination/country/dk.zh-cn.html']



    def parse(self, response):
        # re_selector = response.xpath(r"//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()")
        # print(re_selector)

        booking_continent_item = ItemBookingContinentSpider()
        booking_country_item = ItemBookingCountrySpider()

        continent_id = 1

        try:

            while (continent_id < 100):

                continent_name = response.xpath("//li[@class='dest-sitemap__list-item']//li["+ str(continent_id) + "]//h4[1]/text()").extract()[0].strip()
                print(continent_id, continent_name)

                booking_continent_item["continent_id"] = continent_id
                booking_continent_item["continent_name"] = continent_name
                yield booking_continent_item

                country_id = 1


                try:
                    while (country_id < 1000):
                        # country = response.xpath("//li[@class='dest-sitemap__list-item']//li[2]//div[1]//ul[1]//li[2]//a[1]").extract()[0].strip()
                        country_general_id = country_id + continent_id * 10000
                        country_name = response.xpath("//li[@class='dest-sitemap__list-item']//li[" + str(continent_id) + "]//div[1]//ul[1]//li[" + str(country_id) + "]//a[1]/text()").extract()[0].strip()
                        country_url = response.xpath("//li[@class='dest-sitemap__list-item']//li[" + str(continent_id) + "]//div[1]//ul[1]//li[" + str(country_id) + "]//a[1]//@href").extract()[0]

                        print(continent_id, continent_name, country_general_id, country_name, country_url)

                        country_continent_id = continent_id
                        country_continent_name = continent_name
                        print(country_continent_id, country_continent_name)


                        booking_country_item["country_continent_id"] = country_continent_id
                        booking_country_item["country_continent_name"] = country_continent_name
                        booking_country_item["country_general_id"] = country_general_id
                        booking_country_item["country_name"] = country_name
                        booking_country_item["country_url"] = country_url
                        yield booking_country_item

                        country_id += 1
                except:

                    print(country_name + "国家分析完毕")
                continent_id += 1

                # continent = response.xpath("//li[@class='dest-sitemap__list-item']//li[1]//h4[1]/text()").extract()[0].strip()
                # print(continent)
                # continent_selector = response.xpath("//li[1]//h4[1]/text()")
                # continent = continent_selector.extract()
                # continent_clean =  [x.strip() for x in continent if x.strip() != '']
                # print(continent_clean)

        except:

            print("洲分析完毕")

        pass


