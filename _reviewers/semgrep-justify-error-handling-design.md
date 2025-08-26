---
title: justify error handling design
description: When implementing error handling mechanisms, ensure that design decisions
  are well-justified and properly reasoned. This applies to both architectural choices
  (like global state for error correlation) and technical analysis (like exception
  flow paths).
repository: semgrep/semgrep
label: Error Handling
language: Python
comments_count: 2
repository_stars: 12598
---

When implementing error handling mechanisms, ensure that design decisions are well-justified and properly reasoned. This applies to both architectural choices (like global state for error correlation) and technical analysis (like exception flow paths).

For error correlation systems, clearly document why specific approaches are necessary. For example, when adding global state for tracking failures across system boundaries, explain the correlation requirements that justify the design choice.

For exception handling analysis, ensure proper understanding of control flow and reachability. When exceptions can exit functions early, carefully consider which code paths are actually reachable.

Example from error correlation:
```python
class SemgrepState:
    # Justified: UUID needed for correlating backend requests with failures
    # in fail-open endpoint when semgrep ci fails
    request_id: UUID = Factory(uuid4)
```

Always provide clear reasoning for error handling design decisions, especially when they involve trade-offs like global state or complex control flow analysis.