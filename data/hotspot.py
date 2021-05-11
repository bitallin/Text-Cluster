#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 13:56
# @Author   : Letter
# @Desc     : 
# @File     : hotspot.py
# @Contact  : 5403517@qq.com 
# @Reference:

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import jiagu
from data.record import Record


class Hotspot:
    """
        title:       '北京在中国的北方'
        vec:         np.array
        Keyword:    [('北京', n), ('中国', n),.. ]
    """

    def __init__(self, record: Record):
        """
        Args:
            record:
        """
        self.title = record.text
        self.record_list = [record]
        self.vec = record.vec
        self.record_vec_list = [record.vec]
        self.ranks = len(self.record_list)
        self.keyword = record.keyword
        self.id_list = [record.id_num]  # id is for business requirement

    def append_record(self, record: Record):
        """
            add a record
        Args:
            record:
        Returns:
        """
        self.record_list.append(record)
        self.ranks = len(self.record_list)
        self.record_vec_list.append(record.vec)
        self.id_list.append(record.id_num)

    def append_hotspot(self, hotspot):
        self.record_list.extend(hotspot.record_list)
        self.ranks += hotspot.ranks
        self.record_vec_list.extend(hotspot.record_vec_list)
        self.id_list.extend(hotspot.id_list)

    def get_texts(self):
        return [record.text for record in self.record_list]

    def text_summary(self):
        # TODO sim cal for every text
        _matrix = np.array(self.record_vec_list)
        cos_res = np.sum(cosine_similarity(_matrix, _matrix), axis=-1)
        center_vec_idx = int(np.argmax(cos_res))

        return self.record_list[center_vec_idx].text
