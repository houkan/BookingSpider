

# 基于最新的 UBUNTU镜像
FROM ubuntu:latest
MAINTAINER houkan <hou_kan@hotmail.com>

#更换为国内源 阿里云
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean
RUN  apt-get update
RUN  apt-get -y upgrade

#中文环境设置
ENV LANG C.UTF-8
# ENV LANGUAGE C.UTF-8 #可不配置
# ENV LC_ALL C>UTF-8 #可不配置
RUN  apt-get install -y language-pack-zh-hans
# RUN  locale-gen zh_CN.UTF-8;


#安装数据库支持
RUN  apt-get install -y mysql-server mysql-common mysql-client libmysqlclient-dev

#安装PYTHON环境
RUN  apt-get install -y python3 python3-pip
RUN  ln -s /usr/bin/python3 /usr/bin/python
RUN  ln -s /usr/bin/pip3 /usr/bin/pip

#安装GIT
RUN  apt-get install -y git

#拉取最新的 蜘蛛代码
WORKDIR /root
RUN  git clone -b redis  https://github.com/houkan/BookingSpider.git DistSpider
WORKDIR /root/DistSpider/BookingSpider

#安装蜘蛛需要的 PYTHON 依赖包
RUN  pip install --upgrade pip -i https://pypi.douban.com/simple
RUN  pip install -r requirements.txt -i https://pypi.douban.com/simple


#执行抓取命令
#CMD scrapy runspider spiders/booking.py