# Text cluster

## Quick start
See cluster() in tasks/run_cluster.py

### Example

```python
from tasks.run_cluster import cluster
texts = [.., .., ..]
cluster_res = cluster(texts)
for i in cluster_res:
    print(i.title)
    print(i.ranks)
    print(list(map(lambda x:str(x),i.record_list)))
    print(i.keywords)
```