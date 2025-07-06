---
title: Extract focused functions
description: Break down complex logic into small, well-named functions that each do
  one thing well. This improves code readability, maintainability, and testability
  by making the code's intent clearer and reducing cognitive load.
repository: bridgecrewio/checkov
label: Code Style
language: Python
comments_count: 10
repository_stars: 7667
---

Break down complex logic into small, well-named functions that each do one thing well. This improves code readability, maintainability, and testability by making the code's intent clearer and reducing cognitive load.

Consider this example from discussion #6:

```python
# Before
if "virtual_resources" in vertex.config:
    for i, v in enumerate(self.vertices):
        if v.name in vertex.config["virtual_resources"]:
            self.create_edge(i, origin_node_index, "virtual_resource")

# After
def create_virtual_resources_edges(self, origin_node_index, vertex):
    if "virtual_resources" in vertex.config:
        for i, v in enumerate(self.vertices):
            if v.name in vertex.config["virtual_resources"]:
                self.create_edge(i, origin_node_index, VIRTUAL_RESOURCE_EDGE)
```

Similarly, complex conditions should be extracted into functions with descriptive names:

```python
# Before
if self.bc_integration.repo_matches(file_suppression['repositoryName']) \
        and (suppression_file_path == record_file_path
             or suppression_file_path == convert_to_unix_path(record_file_path)):
    # Do something

# After
def is_matching_suppression_path(self, file_suppression, record_file_path):
    suppression_file_path = normalize_path(file_suppression['filePath'])
    return (self.bc_integration.repo_matches(file_suppression['repositoryName']) 
            and (suppression_file_path == record_file_path
                 or suppression_file_path == convert_to_unix_path(record_file_path)))
```

Apply this principle to:
- Similar code blocks that appear in multiple places
- Complex conditional logic
- Deeply nested loops or conditions
- Code blocks over 5-10 lines
- Logic that can be reused elsewhere

This practice makes code more self-documenting and easier to test, modify, and debug.