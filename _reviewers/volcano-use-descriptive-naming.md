---
title: Use descriptive naming
description: Choose variable, function, and method names that clearly communicate
  their purpose and behavior. Avoid ambiguous abbreviations, numbered suffixes, double
  negatives, and names that don't accurately reflect functionality.
repository: volcano-sh/volcano
label: Naming Conventions
language: Go
comments_count: 11
repository_stars: 4899
---

Choose variable, function, and method names that clearly communicate their purpose and behavior. Avoid ambiguous abbreviations, numbered suffixes, double negatives, and names that don't accurately reflect functionality.

**Key principles:**
- Use descriptive names over abbreviated ones: `preemptorPodPriority` instead of `podPriority`, `candidateHyperNodes` instead of `reScoreHyperNodes`
- Avoid numbered suffixes: `ok` instead of `ok1`
- Eliminate double negatives: use `nodeIsReady` instead of `!nodeIsNotReady`
- Follow Go conventions: use camelCase, not underscores (`filterVictimsFn` not `preemptable_reclaimable_fn`)
- Ensure function names match their behavior: if a function does both predicate and scoring, name it accordingly like `checkNodeGPUSharingPredicateWithScore`

**Example:**
```go
// Poor naming
func (pmpt *Action) taskEligibleToPreemptOthers(preemptor *api.TaskInfo) (bool, string) {
    podPriority := PodPriority(preemptor.Pod)  // Unclear whose priority
    // ...
}

// Better naming  
func (pmpt *Action) taskEligibleToPreemptOthers(preemptor *api.TaskInfo) (bool, string) {
    preemptorPodPriority := PodPriority(preemptor.Pod)  // Clear ownership
    // ...
}
```

Clear naming reduces cognitive load, prevents misunderstandings, and makes code self-documenting for future maintainers.