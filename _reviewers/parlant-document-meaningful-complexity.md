---
title: Document meaningful complexity
description: Documentation should add genuine value by explaining non-obvious behavior,
  complex approaches, or important context that isn't immediately clear from the code
  itself. Remove redundant docstrings and comments that merely restate what the code
  obviously does, while ensuring that sophisticated algorithms, design decisions,
  or non-trivial implementations are...
repository: emcie-co/parlant
label: Documentation
language: Python
comments_count: 2
repository_stars: 12205
---

Documentation should add genuine value by explaining non-obvious behavior, complex approaches, or important context that isn't immediately clear from the code itself. Remove redundant docstrings and comments that merely restate what the code obviously does, while ensuring that sophisticated algorithms, design decisions, or non-trivial implementations are properly documented.

For example, remove obvious documentation like:
```python
class CortexEstimatingTokenizer(EstimatingTokenizer):
    """Token estimator for Cortex."""  # Redundant - class name is self-explanatory
```

But add explanatory documentation for complex approaches:
```python
# This approach works by embedding each capability content separately and using 
# vector similarity search, which is more efficient than retrieving ALL documents 
# and sorting manually because it leverages the database's optimized vector operations
async def find_relevant_capabilities(self, query: str, available_capabilities: Sequence[Capability]):
```

Focus documentation efforts on clarifying the "why" and "how" of complex logic rather than describing the "what" that's already evident from well-written code.