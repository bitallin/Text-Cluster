#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/5/7 11:16
# @Author   : Letter
# @Desc     : Cluster entrypoint file of Samsung opinion data
# @File     : samsung.py
# @Contact  : 5403517@qq.com 
# @Reference:

import os
import time

import pandas as pd

from logs import init_file_logger
from tasks.cluster import TextCluster

logger = init_file_logger('logs/task.log')
labels = ['负面', '正面', '中性']


def merge_xlsx(data_dir='data/raw/all', out_fp='week_report.xlsx'):
    """
        merge all file of data_dir into out_fp
    Args:
        data_dir:
        out_fp:

    Returns:

    """
    fp_list = os.listdir(data_dir)
    df = pd.read_excel('{}/{}'.format(data_dir, fp_list[0]), sheet_name='三星舆情')
    del df['id']
    for data_fp in fp_list[1:]:
        cur_df = pd.read_excel('{}/{}'.format(data_dir, data_fp), sheet_name='三星舆情')
        del cur_df['id']
        df = df.append(cur_df, ignore_index=True)
    df['id'] = list(range(len(df)))
    df.to_excel('{}/{}'.format(data_dir, out_fp), encoding='utf-8-sig', index=False)


def report_cluster(src_xlsx_fp, out_xlsx_dir='data/raw/all'):
    """
        cluster and generate a report xlsx from src_xlsx_fp
    Args:
        src_xlsx_fp:  source data file
        out_xlsx_dir: the xlsx file path of output
    Returns:

    """
    df = pd.read_excel(src_xlsx_fp, index_col=None)
    model = TextCluster(process_num=2, pretrain_wv_fp='data/pretrain_word_embed/500000-small.txt')
    for label in ['负面', '正面', '中性']:
        logger.debug('Start(label:{})'.format(label))
        filter_df = df[df['正负面'] == label]
        texts = list(filter_df['采集标题'].fillna('。') + filter_df['采集内容'])
        ids = list(filter_df['id'].apply(int))

        hotspots = model.cluster_to_hotspot(texts, ids)
        topic_col_name_map = {'正面': 'pos_topic_id', '负面': 'neg_topic_id', '中性': 'neu_topic_id'}
        t_name = topic_col_name_map[label]
        new_df = {'id': [], t_name: [], 'rank': [], 'keywords': [], 'summary': []}

        for topic_idx, hotspot in enumerate(hotspots):
            summary = hotspot.text_summary()

            for record in hotspot.record_list:
                new_df['id'].append(record.id_num)
                new_df[t_name].append(topic_idx)
                new_df['rank'].append(hotspot.ranks)
                new_df['keywords'].append(str(record.keyword))
                new_df['summary'].append(summary)
        new_df = pd.DataFrame(new_df)
        new_df = pd.merge(pd.DataFrame(new_df), df, on='id', how='left')
        time_stick = time.strftime("%Y-%m-%d", time.localtime())
        new_df.to_excel('{}/{}_{}.xlsx'.format(out_xlsx_dir, t_name, time_stick), index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    src_xlsx_fp = 'data/raw/all/week_report.xlsx'
    # pd.read_excel(src_xlsx_fp)
    report_cluster(src_xlsx_fp)
