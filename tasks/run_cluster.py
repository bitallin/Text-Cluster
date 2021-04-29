#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/29 10:33
# @Author   : Letter
# @Desc     : 
# @File     : run_cluster.py
# @Contact  : 5403517@qq.com 
# @Reference:
import pandas as pd

import multiprocessing
from model.cluster_model import TextClusterModel
from model.text2vector import TextVecModel
from typing import List
from utils.util import split_list


class MyManager(multiprocessing.managers.BaseManager):
    pass


def cluster(texts:List[str], w2v_model:TextVecModel):



def cluster_multiprocess(texts: list, process_num: int, pretrain_wv_fp: str):

    # 1. load shared w2v model
    MyManager.register('TextVecModel', TextVecModel)
    manager = MyManager()
    manager.start()
    w2v_model = manager.TextVecModel(pretrain_wv_fp)

    # 2.
    texts = split_list(texts, process_num)

    p_list = [multiprocessing.Process()]

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
                f.write(j + '\n')
            f.write('=================================\n')
