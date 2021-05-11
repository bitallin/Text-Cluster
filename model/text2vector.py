#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/27 11:18
# @Author   : Letter
# @Desc     : word2vec Model (Tencent pretrained word embedding)
# @File     : text2vector.py
# @Contact  : 5403517@qq.com 
# @Reference:

from typing import List

import numpy as np
from LAC import LAC
from gensim.models import KeyedVectors

from data.record import Record
from logs import init_file_logger
from utils.data_preprocess.data_helper import TextClear
import jiagu

logger = init_file_logger()
logger.setLevel('DEBUG')


class TextVecModel:
    def __init__(self, word_vec_fp):
        self.w2v_model = KeyedVectors.load_word2vec_format(word_vec_fp, binary=False)
        self.word_vec_dim = self.w2v_model.vector_size
        self.lac = LAC(mode='lac')
        self.text_help = TextClear()
        self.key_pos_w = {'nz': 1.3, 'nw': 1.3, 'LOC': 1.5, 'PER': 1.7, 'ORG': 1.5, 'n': 1, 's': 1, 'v': 1, 'vn': 1}

    def text2record(self, text: str, id_num: int) -> Record:
        """
            1. text to structure information
            2. convert to Record
        Args:
            text:
        Returns: List[Record]
            Record
        """

        # _text = self.text_help.base_bert_clear(str(text)[:256])

        text = self.text_help.base_bert_clear(str(text))[:256]  # return text after clearing
        try:
            text = '，'.join(jiagu.summarize(text, 2))
        except IndexError as e:
            text = ''.join(jiagu.summarize(text, 1))
        text_vec = np.zeros(self.word_vec_dim)
        _text = self.lac.run([text])[0]
        # [(word, pos, weight), ()]
        _text = [(_text[0][i], _text[1][i], self.key_pos_w[v]) for i, v in enumerate(_text[-1]) if v in self.key_pos_w]
        _text = self.text_help.words_deduplication(_text)
        _flag = False
        word_num = 0
        if len(_text) > 0:
            for item in _text[:7]:  # use 7 keywords
                try:
                    word_vec = self.w2v_model.word_vec(item[0]) * np.array(item[2])
                    text_vec += word_vec
                    _flag = True
                    word_num += 1
                except Exception as e:
                    # logger.debug(e)
                    pass
        if _flag:
            text_vec /= word_num
            return Record(text=text, vec=text_vec, keyword=[(item[0], item[1]) for item in _text[:7]],
                          id_num=id_num)
        else:
            return Record(text=text, vec=None, keyword=None, id_num=id_num)

    def make_records(self, texts: list, ids: list) -> List[Record]:
        data = list(zip(texts, ids))
        texts = list(map(lambda x: self.text2record(x[0], x[1]), data))
        return texts

    def update_key_pos_w(self, k: str, v: float):
        "update the pos weight for computing sentence vector"
        self.key_pos_w[k] = v
        return 1

#
# word_fp = "data/pretrain_word_embed/100000-small.txt"
# t = TextVecModel(word_fp)
# texts = ['2016年初，“世界那么大，想要去看看”在网上爆红，大家都纷纷开始向往诗和远方一个人旅行如何才能拍出美美的游客照？#三星S21#带你重返2016年，告诉你答案～']
# rtn = t.make_records(texts, ids=[1, 2])
# logger.debug(list(map(lambda x: x.keyword, rtn)))
