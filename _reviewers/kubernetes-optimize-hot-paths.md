---
title: Optimize Hot Paths
description: 'When a change affects a scheduler/kubelet hot path, avoid quadratic
  or repeated work: do expensive filtering/KeepOnly/sorting only in the specific variant
  that needs it, and precompute indexes/sorted structures once outside inner loops.
  If the faster algorithm depends on input sizes, make iteration strategy adaptive
  to prevent worst-case slowdowns, and...'
repository: kUbernetes/kUbernetes
label: Performance Optimization
language: Go
comments_count: 6
repository_stars: 128688
---

When a change affects a scheduler/kubelet hot path, avoid quadratic or repeated work: do expensive filtering/KeepOnly/sorting only in the specific variant that needs it, and precompute indexes/sorted structures once outside inner loops. If the faster algorithm depends on input sizes, make iteration strategy adaptive to prevent worst-case slowdowns, and add/adjust benchmarks to confirm throughput or latency improvements.

Do:
- Gate topology-wide or “per-add” work behind the minimal condition that actually requires it (e.g., resize-only where resultDetails is initialized).
- Precompute maps/sorted slices once per evaluation phase; don’t re-sort for every node/pod.
- Pick the iteration direction based on relative sizes (iterate over the smaller side: node labels vs anti-affinity terms).
- Benchmark with representative cluster shapes (vary cardinalities) to ensure improvements don’t regress on common inverses.

Example (gating expensive work to a resize-only path):
```go
func (a *acc) take(cpus cpuset.CPUSet) {
    a.result = a.result.Union(cpus)

    // Only do topology-wide/KeepOnly work when this accumulator is in resize mode.
    if a.resultDetails != nil {
        for _, cpu := range cpus.UnsortedList() {
            if info, ok := a.topo.CPUDetails[cpu]; ok {
                a.resultDetails[cpu] = info
            }
        }
        // KeepOnly should be applied only in resize variants.
        a.resultDetails = a.topo.CPUDetails.KeepOnly(a.result)
    }
}
```

Example (remove repeated sorts by sorting once during state construction):
- Sort victims per node in the phase that builds state, then during scoring just filter condemned victims while preserving relative order—no per-node sort in the scoring loop.

Outcome: lower CPU usage in inner loops, less allocation churn, and fewer performance regressions across different real-world distributions.