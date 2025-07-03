---
title: Unique workflow step names
description: 'When defining CI/CD workflows, always ensure task/step names are unique
  to prevent execution failures. Workflow engines like Argo will reject pipelines
  with duplicate step names, which becomes particularly important when:'
repository: kubeflow/kubeflow
label: CI/CD
language: Python
comments_count: 2
repository_stars: 15064
---

When defining CI/CD workflows, always ensure task/step names are unique to prevent execution failures. Workflow engines like Argo will reject pipelines with duplicate step names, which becomes particularly important when:

1. Building multiple similar artifacts
2. Generating steps programmatically 
3. Reusing step templates

To ensure uniqueness, append identifiers like random strings, build numbers, or artifact identifiers to your step names.

Example:
```python
# Import required libraries
import random
import string

# Define character set for random string generation
alphabet = string.ascii_lowercase + string.digits

# Create unique step name by appending a random string
task["name"] = "base-task-name-" + ''.join(random.choices(alphabet, k=8))
```

This approach ensures each workflow step has a unique identifier while maintaining readability with a consistent prefix, allowing for reliable execution and easier debugging of CI/CD pipelines.
