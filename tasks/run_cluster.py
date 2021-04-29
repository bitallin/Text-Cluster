#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/29 10:33
# @Author   : Letter
# @Desc     : 
# @File     : run_cluster.py
# @Contact  : 5403517@qq.com 
# @Reference:

from multiprocessing import Manager
from multiprocessing import Process
from typing import List

from logs import init_file_logger
from model.cluster_model import TextClusterModel, HotspotClusterModel
from model.text2vector import TextVecModel
from utils.util import split_list

logger = init_file_logger('task.log')


def cluster(texts: List[str], process_num: int, pretrain_wv_fp: str):
    """

    Args:
        texts: list of text
        process_num:   num multiple process
        pretrain_wv_fp: pretrained word vector file
    Returns:
        List[Hotspot]
    """
    # 1. init w2v model
    w2v_model = TextVecModel(pretrain_wv_fp)
    # 2. text cluster
    texts = split_list(texts, process_num)
    model_list = [TextClusterModel(texts[i], w2v_model) for i in range(process_num)]
    shared_res_list = Manager().list([])
    p_list = [Process(target=m.cluster_to, args=(shared_res_list,)) for m in model_list]
    [p.start() for p in p_list]
    [p.join() for p in p_list]
    # 3. hotspot cluster
    logger.info('{} processes finished, shared_res_list length:{}'.format(process_num, len(shared_res_list)))
    while len(shared_res_list) > 1:

        model_list = []
        p_list = []
        single_hotspots = None
        for i in range(0, len(shared_res_list), 2):
            try:
                model_list.append(
                    HotspotClusterModel(hotspots_1=shared_res_list[i], hotspots_2=shared_res_list[i + 1],
                                        ))
            except Exception as e:
                single_hotspots = shared_res_list[-1]
        shared_res_list = Manager().list([])
        if single_hotspots is not None:
            shared_res_list.append(single_hotspots)
        for model in model_list:
            p_list.append(Process(target=model.cluster_to, args=(shared_res_list,)))
        [p.start() for p in p_list]
        [p.join() for p in p_list]
        logger.info('Shared_res_list length:{}'.format(process_num, len(shared_res_list)))
    logger.info('Shared_res_list length:{}'.format(process_num, len(shared_res_list)))
    return shared_res_list[0]


def check():
    wv_fp = 'data/pretrain_word_embed/5000-small.txt'
    texts = ['河南在南方', '河南在南方', '河南在南方', '河南人在南方', '河北在北方', '河北在北方', '河北在北方', '河北在北方', '河北在北方', '河北在北方', '天气不错', '河北在北方',
             '天气不错', '天气很好']
    res = cluster_multiprocess(texts, process_num=4, pretrain_wv_fp=wv_fp)
    print(res)
    print('1')


if __name__ == '__main__':
    check()
