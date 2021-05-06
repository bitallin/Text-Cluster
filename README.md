# Text cluster

## Quick start
See cluster() in tasks/run_cluster.py

### Example

```python
from tasks.cluster import TextCluster
texts = ['北京在北方', '北京在北方', '南京在南方', '南京在南方', '南京在南方', '东京在东方','西北在西北方','西藏在西方']
model = TextCluster(precess_num=2)
model.cluster(texts)
```