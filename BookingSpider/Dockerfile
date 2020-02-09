FROM python:3.7
MAINTAINER houkan <hou_kan@hotmail.com>

ENV PYTHONUNBUFFERED 1
ENV PATH /usr/bin:$PATH
ENV PYTHONPATH "${PYTONPATH}:/"
ENV PYTHONPATH "${PYTONPATH}:/BookingSpider"

RUN mkdir /BookingSpider
WORKDIR /BookingSpider
COPY requirements.txt /BookingSpider/
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
COPY . /BookingSpider/
#WORKDIR /BookingSpider/spiders

CMD scrapy runspider spiders/booking.py