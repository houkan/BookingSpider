# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# TakeFirst取第一个，Join连接

# class BookingSpiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


#
# class BookingItemLoader(ItemLoader):
#     # 自定义itemloader,值取数组的第一个，修改item中的loader
#     default_output_processor = TakeFirst()
#
#
#
#
#
# def return_value(value):
#     # 什么也不做
#     return value
#

class ItemBookingContinentSpider(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    continent_id = scrapy.Field()
    continent_name = scrapy.Field()
    # country_general_id = scrapy.Field()
    # country_name = scrapy.Field()
    # country_url = scrapy.Field()

class ItemBookingCountrySpider(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    country_continent_id = scrapy.Field()
    country_continent_name = scrapy.Field()
    country_general_id = scrapy.Field()
    country_name = scrapy.Field()
    country_url = scrapy.Field()

class ItemBookingCitySpider(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # continent_id = scrapy.Field()
    # continent_name = scrapy.Field()
    # country_general_id = scrapy.Field()
    # country_name = scrapy.Field()
    # country_url = scrapy.Field()
    city_general_id = scrapy.Field()
    city_name = scrapy.Field()
    city_url = scrapy.Field()


