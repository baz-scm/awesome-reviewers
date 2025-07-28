---
title: optimize algorithm performance
description: 'When implementing algorithms, prioritize performance optimization through
  careful algorithm selection, query structure, and evaluation strategy choices. Key
  considerations include:'
repository: logseq/logseq
label: Algorithms
language: Other
comments_count: 5
repository_stars: 37695
---

When implementing algorithms, prioritize performance optimization through careful algorithm selection, query structure, and evaluation strategy choices. Key considerations include:

**Algorithm Selection**: Choose appropriate algorithms for the task. Avoid inefficient patterns like flawed cycle detection that only checks subsets of data or tree walking when more efficient alternatives exist.

**Query Optimization**: Structure database queries and datalog rules for optimal performance. Place filter clauses early in the query to reduce the search space: `(or [?block :logseq.task/scheduled ?n] [?block :logseq.task/deadline ?n]) [(>= ?n ?start-time)] [(<= ?n ?end-time)]` rather than filtering later.

**Evaluation Strategy**: Understand the difference between lazy and eager evaluation. Use `mapv` or `doseq` instead of `map` when side effects are needed, as `map` is lazy and won't execute the operations.

**Rule Optimization**: For recursive queries, carefully order clauses for performance. Write rules optimized for your primary access pattern - descendant queries vs ancestor queries require different clause ordering.

Example of inefficient cycle detection to avoid:
```clojure
;; Problematic - only checks every 100 steps, misses cycles in smaller datasets
(when (and (zero? steps)
           (seq (set/intersection (set @seen) (set uuids-to-add))))
  ;; cycle detection logic
```

Consider computational complexity early in design and choose data structures and algorithms that scale appropriately with expected input sizes.