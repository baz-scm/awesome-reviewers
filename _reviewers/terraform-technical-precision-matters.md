---
title: Technical precision matters
description: 'When documenting algorithms, data structures, and computational processes,
  use precise and objective language rather than subjective assessments. Replace phrases
  like "better approach" with specific technical comparisons that highlight concrete
  differences, such as:'
repository: hashicorp/terraform
label: Algorithms
language: Other
comments_count: 3
repository_stars: 45532
---

When documenting algorithms, data structures, and computational processes, use precise and objective language rather than subjective assessments. Replace phrases like "better approach" with specific technical comparisons that highlight concrete differences, such as:

```
// Instead of this:
// This sorting algorithm is better than bubble sort.

// Write this:
// This merge sort implementation has O(n log n) time complexity compared 
// to bubble sort's O(n²), making it more efficient for large datasets.
```

When providing examples of operations or syntax, maintain consistent formatting and avoid abbreviations for clarity. This precision enables team members to make informed decisions about algorithmic trade-offs and performance characteristics without ambiguity.