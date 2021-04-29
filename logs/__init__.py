#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 13:27
# @Author   : Letter
# @Desc     : 
# @File     : __init__.py
# @Contact  : 5403517@qq.com 
# @Reference:
import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO,
                    format='%(name)s|%(asctime)s|%(filename)s|%(levelname)s|%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )


def init_file_logger(log_fp='logs/task.log'):
    hour_logger = logging.getLogger(log_fp)
    handler_file = TimedRotatingFileHandler(filename=log_fp, when='D', interval=1, backupCount=3, encoding='utf8')
    formatter = logging.Formatter('%(name)s|%(asctime)s|%(filename)s|%(levelname)s|%(message)s',
                                  datefmt='%a, %d %b %Y %H:%M:%S')
    handler_file.setFormatter(formatter)
    hour_logger.addHandler(handler_file)
    return hour_logger
