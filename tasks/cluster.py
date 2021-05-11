#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/29 10:33
# @Author   : Letter
# @Desc     : Cluster entrypoint
# @File     : cluster.py
# @Contact  : 5403517@qq.com 
# @Reference:

from multiprocessing import Manager
from multiprocessing import Process
from typing import List

from data.hotspot import Hotspot
from logs import init_file_logger
from model.cluster_model import TextClusterModel, HotspotClusterModel
from model.text2vector import TextVecModel
from utils.util import split_list

logger = init_file_logger('logs/task.log')


class TextCluster:
    def __init__(self, process_num, pretrain_wv_fp='data/pretrain_word_embed/100000-small.txt', ):
        self.w2v_model = TextVecModel(pretrain_wv_fp)
        self.process_num = process_num
        self.pretrain_wv_fp = pretrain_wv_fp

    def cluster_to_hotspot(self, texts_list, top_k, kw_num, text_sim_threshold, topic_sim_threshold) -> List[Hotspot]:
        texts_list = split_list(texts_list, self.process_num)
        model_list = [TextClusterModel(texts=texts_list[i], vec_model=self.w2v_model, kw_num=kw_num,
                                       sim_threshold=text_sim_threshold) for i in
                      range(self.process_num)]
        shared_res_list = Manager().list([])
        p_list = [Process(target=m.cluster_to, args=(shared_res_list,)) for m in model_list]
        [p.start() for p in p_list]
        [p.join() for p in p_list]
        # 3. hotspot cluster
        logger.info('{} processes finished, shared_res_list length:{}'.format(self.process_num, len(shared_res_list)))
        while len(shared_res_list) > 1:
            model_list = []
            p_list = []
            single_hotspots = None
            for i in range(0, len(shared_res_list), 2):
                try:
                    model_list.append(
                        HotspotClusterModel(hotspots_1=shared_res_list[i], hotspots_2=shared_res_list[i + 1],
                                            sim_threshold=topic_sim_threshold,
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
            logger.info('Shared_res_list length:{}'.format(self.process_num, len(shared_res_list)))
        logger.info('Shared_res_list length:{}'.format(self.process_num, len(shared_res_list)))
        return sorted(shared_res_list[0], key=lambda x: x.ranks, reverse=True)[:top_k]

    def cluster(self, texts, top_k, kw_num=7, text_sim_threshold=0.9, topic_sim_threshold=0.88):
        rtn = []
        hotspots = self.cluster_to_hotspot(texts, top_k, kw_num, text_sim_threshold, topic_sim_threshold)
        for idx, item in enumerate(hotspots):
            rtn.append({'topic_num': idx + 1, 'rank': item.ranks, 'keywords': item.keyword,
                        'texts': [r.text for r in item.record_list]})
        return rtn

    @staticmethod
    def hotspots_to_file(hotspots: List[Hotspot], out_fp: str):
        with open(out_fp, 'w', encoding='utf8') as f:
            f.write('Topic num:{}\n'.format(len(hotspots)))
            f.write('=' * 30 + '\n' + '\n')
            for idx, item in enumerate(hotspots):
                f.write('=' * 8 + 'Topic {}'.format(idx) + '=' * 8 + '\n')
                f.write("Rank:{}\n".format(item.ranks))
                f.write("Keywords:{}\n".format(item.keyword))
                f.write("Texts:\n")
                for i in item.record_list:
                    f.write(str(i) + '\n')
                f.write('=' * 30 + '\n')
