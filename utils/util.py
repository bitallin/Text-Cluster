#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/29 10:52
# @Author   : Letter
# @Desc     : 
# @File     : util.py
# @Contact  : 5403517@qq.com 
# @Reference:
from math import ceil


def split_list(li, n):
    assert len(li) >= 2 * n, 'len(li) should be greater equal than n'
    per_num = ceil(len(li) / n)
    return [li[i:i + per_num] for i in range(0, len(li), per_num)]



