#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/5/11 15:26
# @Author   : Letter
# @Desc     : 
# @File     : test_func.py
# @Contact  : 5403517@qq.com 
# @Reference:

import unittest
from tasks.cluster import TextCluster


class TestCluster(unittest.TestCase):
    def setUp(self) -> None:
        self.texts = ['北京在北方', '北京在北方', '南京在南方', '南京在南方', '南京在南方', '东京在东方', '西北在西北方', '西藏在西方']
        self.model = TextCluster(process_num=2)

    def test_cluster(self):
        res = self.model.cluster(self.texts, top_k=20, kw_num=7)
        print(res)
