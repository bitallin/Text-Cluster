# Text cluster

## Quick start
See cluster() in tasks/run_cluster.py

### Example

```python
from tasks.run_cluster import cluster
texts = ['北京在北方', '北京在北方', '南京在南方', '南京在南方', '南京在南方', ]
cluster_res = cluster(texts, process_num=2, pretrain_wv_fp='data/pretrain_word_vec/5000-small.txt')
for i in cluster_res:
    print(i.title)
    print(i.ranks)
    print(list(map(lambda x:str(x),i.record_list)))
    print(i.keywords)
```