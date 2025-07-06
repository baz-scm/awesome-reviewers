---
title: Choose optimal data structures
description: 'Select the most appropriate data structure based on the specific operations
  your algorithm needs to perform. This choice can dramatically impact performance
  and code clarity:'
repository: bridgecrewio/checkov
label: Algorithms
language: Python
comments_count: 5
repository_stars: 7668
---

Select the most appropriate data structure based on the specific operations your algorithm needs to perform. This choice can dramatically impact performance and code clarity:

1. Use sets instead of lists when you need unique values or fast membership testing:
```python
# Instead of checking membership in a list (O(n) operation):
ENTROPY_CHECK_IDS = ('CKV_SECRET_6', 'CKV_SECRET_19', 'CKV_SECRET_80')
if check_id in ENTROPY_CHECK_IDS:  # Linear search

# Use a set for O(1) lookups:
ENTROPY_CHECK_IDS = {'CKV_SECRET_6', 'CKV_SECRET_19', 'CKV_SECRET_80'}
if check_id in ENTROPY_CHECK_IDS:  # Constant-time lookup
```

2. Consider defaultdict to simplify code that manages collections:
```python
# Instead of manually checking if keys exist:
dirs_to_definitions = {}
for tf_definition_key, tf_value in tf_definitions.items():
    dir_path = os.path.dirname(tf_definition_key.file_path)
    if dir_path in dirs_to_definitions:
        dirs_to_definitions[dir_path].append({tf_definition_key: tf_value})
    else:
        dirs_to_definitions[dir_path] = [{tf_definition_key: tf_value}]

# Use defaultdict for automatic initialization:
from collections import defaultdict
dirs_to_definitions = defaultdict(list)
for tf_definition_key, tf_value in tf_definitions.items():
    dir_path = os.path.dirname(tf_definition_key.file_path)
    dirs_to_definitions[dir_path].append({tf_definition_key: tf_value})
```

3. When implementing search algorithms, use early termination when possible:
```python
# Instead of collecting all matches and then choosing one:
target_variables = [
    index for index in variables_map.get(vertex.name, [])
    if conditions_match(index)
]
if len(target_variables) >= 1:
    use_variable(target_variables[0])

# Stop once you find what you need:
target_variable = 0
for index in variables_map.get(vertex.name, []):
    if conditions_match(index):
        target_variable = index
        break
if target_variable:
    use_variable(target_variable)
```

Choosing the right data structure is fundamental to writing efficient algorithms and clear code.