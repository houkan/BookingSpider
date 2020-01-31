# -*- coding: utf-8 -*-
# @Author   : Ken Hou
# @Time     : 2019-12-22 23:25
# @File     : main.py
# @Software : PyCharm
# @Project  : BookingSpider
# @User     : kan
# ----------------------------

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# execute (["scrapy","crawl","booking"])
# execute (["scrapy","crawl","bookingcity"])
# execute (["scrapy","crawl","bookinghotel"])
# execute (["scrapy","crawl","bookinghoteldetail"])
execute (["scrapy","crawl","bookinghoteldetailjs"])
