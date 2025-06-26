---
title: "Optimize data structure selection"
description: "Choose data structures that match your specific access patterns and performance requirements. The right data structure can significantly improve performance without requiring algorithm changes."
repository: "vercel/next.js"
label: "Performance Optimization"
language: "Rust"
comments_count: 3
repository_stars: 133000
---

Choose data structures that match your specific access patterns and performance requirements. The right data structure can significantly improve performance without requiring algorithm changes.

For concurrent access patterns, consider specialized concurrent data structures:
```rust
// Instead of this
subscribers: Arc<Mutex<HashMap<String, Vec<mpsc::Sender<Arc<dyn CompilationEvent>>>>>>,

// Consider this for better concurrent performance
subscribers: DashMap<String, Vec<mpsc::Sender<Arc<dyn CompilationEvent>>>>,
```

For data storage, evaluate compression benefits with appropriate thresholds:
```rust
// Consider compression only when beneficial
if bytes.len() > MIN_COMPRESSION_SIZE && compressed.len() < bytes.len() {
    Compressed(compressed)
} else {
    Local(bytes)
}
```

For serialization/deserialization, minimize allocations using stack allocation for small values:
```rust
// Instead of always allocating on the heap
struct Data(Vec<u8>, IndexSet<RcStr, FxBuildHasher>);

// Consider stack allocation for small values
struct SerData(SmallVec<[u8; 16]>, FxIndexSet<RcStr>);
```

Always measure the performance impact of your choices with benchmarks to confirm expected improvements. As seen in real examples, the right data structure can yield performance improvements of 3x or more in high-throughput scenarios.