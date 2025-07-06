---
title: Choose optimal algorithms
description: Always select appropriate data structures and algorithms based on their
  performance characteristics and the specific operations your code needs to perform.
  This can significantly improve both code readability and execution efficiency.
repository: bridgecrewio/checkov
label: Algorithms
language: Python
comments_count: 8
repository_stars: 7667
---

Always select appropriate data structures and algorithms based on their performance characteristics and the specific operations your code needs to perform. This can significantly improve both code readability and execution efficiency.

For data structures:
- Use sets instead of lists when checking for membership or ensuring uniqueness, as they provide O(1) average lookup time:
```python
# Instead of:
secret_suppressions_id = [suppression['policyId'] for suppression in suppressions]

# Use:
secret_suppressions_id = {suppression['policyId'] for suppression in suppressions}
```

- Use defaultdict when initializing dictionaries that need default values for missing keys:
```python
# Instead of:
if dir_path in dirs_to_definitions:
    dirs_to_definitions[dir_path].append({tf_definition_key: tf_value})
else:
    dirs_to_definitions[dir_path] = [{tf_definition_key: tf_value}]

# Use:
from collections import defaultdict
dirs_to_definitions = defaultdict(list)
dirs_to_definitions[dir_path].append({tf_definition_key: tf_value})
```

For algorithms:
- Optimize search operations by starting from known positions or using early termination:
```python
# Instead of searching the entire file:
def find_line_number(file_string: str, substring: str, default_line_number: int) -> int:
    # Start from default_line_number and stop when found
    # instead of scanning the entire file
```

- Use more efficient iteration patterns:
```python
# Instead of:
for field in each["change"]["before"]:
    if each["change"]["before"][field] != each["change"]["after"].get(field):

# Use:
for field, value in each["change"]["before"].items():
    if value != each["change"]["after"].get(field):
```

- Avoid regular expressions with potential for exponential backtracking, especially on large inputs

When in doubt, use specialized libraries that implement optimized algorithms (e.g., for version comparison) rather than implementing your own solutions.