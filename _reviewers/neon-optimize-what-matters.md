---
title: Optimize what matters
description: Focus optimization efforts on performance-critical paths rather than
  applying micro-optimizations everywhere. Balance code clarity and maintainability
  against performance gains, and only optimize when there's a measurable benefit.
repository: neondatabase/neon
label: Performance Optimization
language: C
comments_count: 2
repository_stars: 19015
---

Focus optimization efforts on performance-critical paths rather than applying micro-optimizations everywhere. Balance code clarity and maintainability against performance gains, and only optimize when there's a measurable benefit.

When considering optimizations:
1. Determine if the code is on a critical path or frequently executed
2. Measure the actual performance impact before and after changes
3. Evaluate the tradeoff between readability and performance

For example, avoid premature optimization in code like this:

```c
// PREFER: Simple and clear approach for non-critical code
for (int bucketno = 0; bucketno < NUM_QT_BUCKETS; bucketno++) {
    uint64 threshold = qt_bucket_thresholds[bucketno];
    metrics[i].bucket_le = (threshold == UINT64_MAX) ? INFINITY : ((double) threshold) / 1000000.0;
}

// AVOID: Premature optimization making code less clear
for (int bucketno = 0; bucketno < NUM_QT_BUCKETS - 1; bucketno++) {
    metrics[i].bucket_le = ((double) qt_bucket_thresholds[bucketno]) / 1000000.0;
}
// Special case for last bucket
metrics[NUM_QT_BUCKETS-1].bucket_le = INFINITY;
```

However, when there's significant performance impact (like looping from 3 to INT_MAX), optimization becomes necessary. Always document performance-critical sections and the rationale behind optimization decisions.