---
title: Algorithm specification compliance
description: When implementing layout algorithms, ensure strict adherence to web standards
  and specifications, particularly regarding control flow and edge case handling.
  Complex algorithms like baseline calculation require precise implementation of specification
  details to avoid subtle bugs.
repository: facebook/yoga
label: Algorithms
language: C
comments_count: 3
repository_stars: 18255
---

When implementing layout algorithms, ensure strict adherence to web standards and specifications, particularly regarding control flow and edge case handling. Complex algorithms like baseline calculation require precise implementation of specification details to avoid subtle bugs.

Key considerations:
- Use correct loop control (`break` vs `continue`) to match specification behavior
- Implement proper selection logic for algorithm steps (e.g., "first baseline aligned child, otherwise last child")
- Apply axis-specific calculations where required by the specification
- Validate algorithm behavior against reference implementations

Example from baseline calculation:
```c
// Wrong: continues past first line, skipping valid children
if (child->lineIndex > 0) {
    continue;  // This skips children incorrectly
}

// Correct: breaks at first line boundary as per spec
if (child->lineIndex > 0) {
    break;  // Only consider first line children
}
```

This prevents algorithmic errors that can cause incorrect layout behavior and ensures compatibility with web standards.