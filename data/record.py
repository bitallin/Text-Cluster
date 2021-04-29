#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 12:04
# @Author   : Letter
# @Desc     : 
# @File     : record.py
# @Contact  : 5403517@qq.com 
# @Reference:

import numpy as np


class Record:
    """
        text:       '北京在中国的北方'
        vecL:       np.array
        Keyword:    [('北京', n), ('中国', n),.. ]
    """
    def __init__(self, text, vec: np.ndarray = None, keyword: list = None):
        self.text = text
        self.vec = vec
        self.keyword = keyword

    def __str__(self):
        return self.text
