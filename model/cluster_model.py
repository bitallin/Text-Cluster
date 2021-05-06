#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 13:53
# @Author   : Letter
# @Desc     : function of text cluster
# @File     : cluster_model.py
# @Contact  : 5403517@qq.com 
# @Reference:


from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from data.hotspot import Hotspot
from logs import init_file_logger
from model.text2vector import TextVecModel

logger = init_file_logger()


class TextClusterModel:
    """
        text cluster
    """

    def __init__(self, texts: List[str], vec_model: TextVecModel, top_k: int = 1000,
                 sim_threshold: float = 0.93, ):

        # self.vec_model = vec_model   # Current paddle do not support multiprocess for pickle
        logger.info('W2V Model has been initialized successfully!')
        record_list = vec_model.make_records(texts)
        logger.info('Texts to Records, finished.')
        self.sim_threshold = sim_threshold
        self.top_k = top_k
        self.records = [record for record in record_list if record.vec is not None]

    def run(self) -> List[Hotspot]:
        hotspot_list = [Hotspot(self.records[0])]
        hotspot_vecs = np.array([hotspot_list[0].vec])
        for record in self.records[1:]:
            sim = cosine_similarity(record.vec.reshape(1, -1), hotspot_vecs)[0]
            max_sim_idx = int(np.argmax(sim))
            max_sim_value = sim[max_sim_idx]
            if max_sim_value >= self.sim_threshold:
                hotspot_list[max_sim_idx].append_record(record)
            else:
                hotspot_list.append(Hotspot(record))
                hotspot_vecs = np.vstack((hotspot_vecs, record.vec))
        hotspot_list = sorted(hotspot_list, key=lambda x: x.ranks, reverse=True)[:self.top_k]
        return hotspot_list

    @staticmethod
    def parse_hotspots(hotspots: List[Hotspot]) -> list:
        return [{'texts': hotspot.get_texts(), 'rank': hotspot.ranks} for hotspot in hotspots]

    def cluster_to(self, global_var_list: List[Hotspot]):
        res = self.run()
        global_var_list.append(res)


class HotspotClusterModel:
    """
        2 hotspot group cluster
    """

    def __init__(self, hotspots_1: List[Hotspot], hotspots_2: List[Hotspot], top_k: int = 1000,
                 sim_threshold: float = 0.88, ):

        self.hotspot_1 = hotspots_1
        self.hotspot_2 = hotspots_2
        self.sim_threshold = sim_threshold
        self.top_k = top_k

    def run(self) -> List[Hotspot]:

        hotspots_vecs = np.array([hotspot.vec for hotspot in self.hotspot_1])
        for hotspot in self.hotspot_2:
            sim = cosine_similarity(hotspot.vec.reshape(1, -1), hotspots_vecs)[0]
            max_sim_idx = int(np.argmax(sim))
            max_sim_value = sim[max_sim_idx]
            if max_sim_value >= self.sim_threshold:
                self.hotspot_1[max_sim_idx].append_hotspot(hotspot)
            else:
                self.hotspot_1.append(hotspot)
                hotspots_vecs = np.vstack((hotspots_vecs, hotspot.vec))
        hotspot_list = sorted(self.hotspot_1, key=lambda x: x.ranks, reverse=True)[:self.top_k]
        return hotspot_list

    @staticmethod
    def parse_hotspots(hotspots: List[Hotspot]) -> list:
        return [{'texts': hotspot.get_texts(), 'rank': hotspot.ranks} for hotspot in hotspots]

    def cluster_to(self, global_var_list: List[Hotspot]):
        res = self.run()
        global_var_list.append(res)
