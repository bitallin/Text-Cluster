# Text cluster

## Quick start
See TextCluster class in tasks/cluster.py

### Example

```python
from tasks.cluster import TextCluster
texts = ['北京在北方', '北京在北方', '南京在南方', '南京在南方', '南京在南方', '东京在东方','西北在西北方','西藏在西方']
model = TextCluster(process_num=2, top_k=20)
model.cluster(texts)
Out:[{'topic_num': 1,
	  'rank': 3,
	  'keywords': [('南京', 'LOC'), ('南方', 's')],
	  'texts': ['南京在南方', '南京在南方', '南京在南方']},
	 {'topic_num': 2,
	  'rank': 2,
	  'keywords': [('北京', 'LOC'), ('北方', 's')],
	  'texts': ['北京在北方', '北京在北方']},
	 {'topic_num': 3,
	  'rank': 1,
	  'keywords': [('东京', 'LOC'), ('东方', 's')],
	  'texts': ['东京在东方']},
	 {'topic_num': 4,
	  'rank': 1,
	  'keywords': [('西藏', 'LOC'), ('西方', 's')],
	  'texts': ['西藏在西方']}]
```