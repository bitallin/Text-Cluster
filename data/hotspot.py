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
    """
        title:       '北京在中国的北方'
        vec:         np.array
        Keyword:    [('北京', n), ('中国', n),.. ]
    """
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

    def append_record(self, record: Record):
        """
            add a record
        Args:
            record:
        Returns:
        """
        self.record_list.append(record)
        self.ranks = len(self.record_list)

    def append_hotspot(self, hotspot):
        self.record_list.extend(hotspot.record_list)
        self.ranks += hotspot.ranks

    def get_texts(self):
        return [record.text for record in self.record_list]
