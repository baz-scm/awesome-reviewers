---
title: Data structure correctness
description: 'Ensure data structures are accurately represented with their proper
  constraints and valid implementations, particularly for recursive structures. When
  documenting or implementing collections:'
repository: pydantic/pydantic
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 24377
---

Ensure data structures are accurately represented with their proper constraints and valid implementations, particularly for recursive structures. When documenting or implementing collections:

1. Explicitly state data structure constraints
   - For set-like structures, clearly document hashability requirements
   - For tree-like structures, describe node relationships precisely

2. Validate that recursive type examples actually terminate
   - Include escape conditions in recursive type definitions
   - Ensure examples represent structures that can be instantiated

```python
# Incorrect recursive type definition (infinite recursion)
type B = list[C]
type C = B  # No termination condition!

# Correct recursive type definition with termination
type A = list[A] | None  # Terminates with None
```

Properly defined data structures not only prevent runtime errors but also enable more efficient algorithm implementations.