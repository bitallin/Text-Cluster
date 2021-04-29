#!/usr/bin/env python
# encoding: utf-8
"""
    @Time: 2021/4/9 15:32
    @File: data_helper.py
    @Desc:
    @Reference: 
    @Author: letter
    @Contact: 5403517@qq.com
"""

import re

from utils.data_preprocess.data.langconv import *


class TextClear:
    def __init__(self):
        # 加载正则编译器
        """
            如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始。
            而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。
        """
        self.re_que_punc = re.compile(r"[?？]+")
        self.re_cn = re.compile(r'[\u4e00-\u9fa5]')
        self.re_time = re.compile(r"\d+-\d+-\d+\s+\d+:\d+")

        self.re_punc = re.compile(
            r"[,.，–\'。≧▽ω≦з」∠＝｜|／°^＜＞〉{}．😊😄ㄛ丨⋯％😭😳😠；*＂=－『』😍「→～—￥＋×∩╭╮`~$%…&:：!！【】@‘’“”\-_\\/、\]\[#+~·《》()（）]+")

        self.re_eng = re.compile(r'[a-zA-Z]+')
        self.re_float = re.compile(r'\d+\.\d+')
        self.re_digit = re.compile(r'\d+')
        self.re_http = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.re_forward = re.compile("@.*?: ", re.S)
        self.re_emoji = re.compile(r"\[.*?]", re.S)
        self.re_at = re.compile("@.*?( |:)", re.S)
        self.re_yuanweibo = re.compile(r"【原微博】", re.S)
        self.re_http_tag = re.compile(r"<.*>")

        self.re_hard = re.compile(r"​​", re.S)

    def clear_for_words(self, sentence):
        '''

            :param text_list:  ["一段文本", "第二段文本"]
            :return:           同上
        '''

        # the precess is ordered
        # remove  < >
        sentence = self.base_bert_clear(sentence, seq_len=512)
        sentence = sentence.replace('<', '《').replace('>', '》').replace(' ', '')
        sentence = sentence.lower().replace('samsung', '三星').replace('xiaomi', '小米').replace('huawei', '华为') \
            .replace('apple', '苹果').replace('honor', '荣耀').replace('redmi', '红米') \
            .replace('meizu', '魅族').replace('sanxing', '三星') \
            .replace('Galaxy', '三星盖乐世').replace('iphone', '苹果手机')
        sentence = re.sub(self.re_eng, '<eng>', sentence)
        sentence = re.sub(self.re_float, '<flt>', sentence)
        sentence = re.sub(self.re_digit, '<dgt>', sentence)
        sentence = re.sub(self.re_punc, '<punc>', sentence)
        sentence = re.sub(self.re_que_punc, '<que>', sentence)
        return sentence

    def base_bert_clear(self, sentence, seq_len=128):
        """
        clear text for bert
        Args:
            sentence:
            seq_len:
        Returns:
        """
        sentence = self.tradition_to_simple(sentence)
        sentence = re.sub(self.re_hard, "", sentence)
        sentence = self.delete_http_tag(sentence)
        sentence = self.delete_none(sentence)
        sentence = self.delete_emoji(sentence)
        sentence = self.delete_at(sentence)
        sentence = self.delete_http(sentence)

        return sentence[:seq_len]

    def replace_eng(self, sentence):
        sentence = re.sub(self.re_eng, 'e', sentence)
        return sentence

    def delete_http_tag(self, sentence):
        sentence = re.sub(self.re_http_tag, '', sentence)
        return sentence

    @staticmethod
    def delete_zhuanfa(sentence):
        sentence = re.sub(r"转发微博", "", sentence)
        return sentence

    def delete_time(self, sentence):
        sentence = re.sub(self.re_time, "", sentence)
        return sentence

    def delete_at(self, sentence):
        sentence = re.sub(self.re_at, "", sentence)
        return sentence

    @staticmethod
    def delete_none(sentence: str):
        """删除空白,空格"""
        return sentence.replace(' ', '').replace('\t', '').replace('</br>', '').replace('\u200b', '').replace('\n', '，')

    def delete_http(self, sentence):
        sentence = re.sub(self.re_http, "", sentence)
        return sentence

    def delete_emoji(self, sentence):
        return re.sub(self.re_emoji, "", sentence)

    @staticmethod
    def tradition_to_simple(text: str):
        """繁体转简体"""
        text = Converter('zh-hans').convert(text)
        return text

    @staticmethod
    def wordsDeduplication(word_list: list):
        """
            词去重
        Args:
            word_list: ['中华民族伟大', '民族伟大']
        Returns:
            list: ['中华民族伟大']
        """
        # 先set去重，按照长度降序
        word_list = sorted(list(set(word_list)), key=lambda x: len(x), reverse=True)
        words_num = len(word_list)
        if words_num < 2:
            # 判断词的个数
            return word_list

        rtn_word_list = []
        for i in range(words_num):
            for j in range(words_num):
                if i == j:  # 不和自身比较
                    continue
                if word_list[i] in word_list[j]:
                    # 和其他词比较是否重复
                    # 如果重复，直接跳出，不保存该词
                    break
            # 无重复，保存该词
            if j == words_num - 1:
                rtn_word_list.append(word_list[i])

        return rtn_word_list


# t = TextClear()
