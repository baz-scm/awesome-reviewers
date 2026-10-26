---
title: Null-safe initialization and validation
description: When dealing with optional fields, feature-gated behavior, or value-or-valueFrom
  unions, nil safety must be structural—not dependent on caller ordering or duplicated
  guards.
repository: kUbernetes/kUbernetes
label: Null Handling
language: Go
comments_count: 6
repository_stars: 128688
---

When dealing with optional fields, feature-gated behavior, or value-or-valueFrom unions, nil safety must be structural—not dependent on caller ordering or duplicated guards.

**Standard rules**
1. **Fully initialize objects before any early return**
   - If a constructor can return early, ensure all fields that any method might read are initialized first (empty maps/structs, default comparators/sorters, etc.), or make returned objects impossible to misuse.

2. **Never dereference union “either/or” fields without proving the case**
   - If a struct represents `Value` OR `ValueFrom`, treat the other side as potentially nil.
   - Either filter out entries where `Value` is nil before dereferencing, or use a nil-safe deref helper.

3. **Guard nil receivers when behavior depends on feature gates**
   - If a field can be nil under a feature gate (e.g., opportunistic batching disabled), check `if obj != nil` before calling methods, or make the method explicitly nil-safe.

4. **Represent “unset” vs “set to zero” with pointer types**
   - If zero is meaningful, use pointers in the API types and conversions so absence and explicit zero are distinguishable.
   - Ensure JSON/proto tags use `omitempty` when appropriate to avoid emitting `null`.

5. **Validate required subfields before using them for logic (dedupe/comparisons)**
   - When validation needs to check duplicates/compatibility, don’t branch on optional fields that may be missing; let declarative validation report the missing fields first, then apply additional logic.

**Example patterns**
```go
// 1) Constructor: initialize before early return
acc := &cpuAccumulator{
  logger: logger,
  topo: topo,
  details: topo.CPUDetails.KeepOnly(availableCPUs),
  result: cpuset.New(),
  resultDetails: topology.CPUDetails{},
  // init everything methods might rely on
  numaOrSocketsFirst: ...,
  availableCPUSorter: ...,
}
if numCPUs == currentlyAllocatedCPUs.Size() {
  acc.take(currentlyAllocatedCPUs.Clone())
  return acc
}

// 2) Union: never deref c.Value unless ValueFrom is absent
if c.ValueFrom != nil {
  // handle/skip/filter; do not deref c.Value
} else if c.Value != nil {
  quantity := c.Value.DeepCopy()

// 3) Feature-gated nil receiver
if f.batch != nil {
  f.batch.SetDisabled(true)
}
```

Applying these rules prevents panics and semantic drift caused by nil fields, feature-skewed objects, and ambiguous “zero vs unset” cases.