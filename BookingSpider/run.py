# -*- coding: utf-8 -*-
# @Author   : Ken Hou
# @Time     : 2019-12-27 23:27
# @File     : run.py
# @Software : PyCharm
# @Project  : BookingSpider
# @User     : kan
# ----------------------------

from scrapy.cmdline import execute


# execute(['scrapy','crawl','booking'])
# execute(['scrapy','crawl','bookingcity'])
# execute(['scrapy','crawl','bookinghotel'])
# execute(['scrapy','crawl','bookinghoteldetail'])
execute(['scrapy','crawl','bookinghoteldetailjs'])

