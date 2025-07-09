---
title: Consistent configuration declarations
description: Ensure configuration specifications (such as version requirements, environment
  settings, and tool declarations) are consistent and not duplicated across project
  files. Redundant or contradictory configuration declarations create maintenance
  issues and confusion.
repository: crewaiinc/crewai
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 33945
---

Ensure configuration specifications (such as version requirements, environment settings, and tool declarations) are consistent and not duplicated across project files. Redundant or contradictory configuration declarations create maintenance issues and confusion.

For example, instead of declaring the same tool in multiple places:

```yaml
# agents.yaml
tools:
  - SerperDevTool  # Don't declare here if also declared in crew.py
```

```python
# crew.py
# Declare tools in a single location
tools = [SerperDevTool()]
```

Similarly, ensure version specifications in documentation accurately reflect actual compatibility:

```markdown
# README.md
Ensure you have Python >=3.10 <3.12 installed on your system.
```

When the project actually supports Python 3.12, this should be correctly documented as:

```markdown
# README.md
Ensure you have Python >=3.10 <=3.12 installed on your system.
```