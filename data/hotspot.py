#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 13:56
# @Author   : Letter
# @Desc     : 
# @File     : hotspot.py
# @Contact  : 5403517@qq.com 
# @Reference:

from data.record import Record


class Hotspot:
    def __init__(self, record: Record):
        """
            initialize through one record
        Args:
            record:
        """
        self.title = record.text
        self.record_list = [record]
        self.vec = record.vec
        self.ranks = len(self.record_list)
        self.keyword = record.keyword

    def update(self, record: Record):
        """
            add a record
        Args:
            record:
        Returns:
        """
        self.record_list.append(record)
        self.ranks = len(self.record_list)

    def get_texts(self):
        return [record.text for record in self.record_list]
