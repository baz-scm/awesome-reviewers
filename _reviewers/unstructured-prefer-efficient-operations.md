---
title: prefer efficient operations
description: Choose efficient operations and algorithms over expensive alternatives,
  particularly when processing data or performing file operations. Avoid operations
  that create unnecessary intermediate objects or make repeated system calls when
  vectorized or batch operations are available.
repository: Unstructured-IO/unstructured
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 12116
---

Choose efficient operations and algorithms over expensive alternatives, particularly when processing data or performing file operations. Avoid operations that create unnecessary intermediate objects or make repeated system calls when vectorized or batch operations are available.

Key principles:
- Use vectorized operations instead of loops when working with data structures like pandas DataFrames
- Avoid expensive string operations like `split()` when simple slicing suffices
- Minimize repeated system calls by batching operations or using single calls that return multiple results

Examples:
```python
# Instead of computing values in a loop:
for item in items:
    item['width'] = item['right'] - item['left']
    item['height'] = item['bottom'] - item['top']

# Use vectorized operations:
df['width'] = df['right'] - df['left'] 
df['height'] = df['bottom'] - df['top']

# Instead of expensive string splitting:
filename = (doc.split("/")[-1]).split(f".{output_type}")[0]

# Use efficient slicing:
filename = os.path.basename(doc)[:-len(output_type)-1]

# Instead of repeated system calls:
while os.path.exists(os.path.join(dir, filename)):
    # check and increment

# Use single directory listing:
existing_files = os.listdir(dir)
# then filter and find max counter
```

This approach reduces computational overhead, memory allocation, and system call frequency, leading to better overall performance.