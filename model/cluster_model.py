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
from model.text2vector import TextVecModel
from logs import init_file_logger
import pandas as pd

logger = init_file_logger()


class TextClusterModel:
    def __init__(self, texts: List[str], vec_fp: str = 'data/pretrain_word.embed', top_k: int = 1000,
                 sim_threshold: float = 0.7, ):

        self.w2v_model = TextVecModel(word_vec_fp=vec_fp)
        logger.info('W2V Model has been initialized successfully!')
        record_list = self.w2v_model.make_records(texts)
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
                hotspot_list[max_sim_idx].update(record)
            else:
                hotspot_list.append(Hotspot(record))
                hotspot_vecs = np.vstack((hotspot_vecs, record.vec))
        hotspot_list = sorted(hotspot_list, key=lambda x: x.ranks, reverse=True)[:self.top_k]
        return hotspot_list

    @staticmethod
    def parse_hotspots(hotspots: List[Hotspot]) -> list:
        return [{'texts': hotspot.get_texts(), 'rank': hotspot.ranks} for hotspot in hotspots]


def check():
    wv_fp = 'data/pretrain_word_embed/100000-small.txt'
    data_fp = 'data/ss_report.xlsx'
    df = pd.read_excel(data_fp)
    texts = df['采集内容']
    cluster_model = TextClusterModel(texts, wv_fp, 10, 0.85)
    hotspots = cluster_model.run()
    res = cluster_model.parse_hotspots(hotspots)

    fp = 'data/res.log'
    with open(fp, 'w', encoding='utf8') as f:
        for i in res:
            for j in i['texts']:
                f.write(j+'\n')
            f.write('=================================\n')



check()
