---
title: Choose optimal data structures
description: 'Select data structures based on specific access patterns and performance
  requirements. When both fast lookup and predictable iteration order are needed,
  specialized structures like IndexMap offer benefits over standard HashMap:'
repository: influxdata/influxdb
label: Algorithms
language: Rust
comments_count: 6
repository_stars: 30268
---

Select data structures based on specific access patterns and performance requirements. When both fast lookup and predictable iteration order are needed, specialized structures like IndexMap offer benefits over standard HashMap:

```rust
// When order matters and lookups are frequent:
use indexmap::IndexMap;

// Fast lookups + preserved insertion order
let cache: IndexMap<String, CacheColumn> = IndexMap::new();

// Regular HashMap when only lookup speed matters
let simple_lookup: HashMap<String, Value> = HashMap::new();
```

For serialization, separate concerns from runtime efficiency - use simple Vector structures for serialization, then transform into Maps for runtime lookups. This avoids serializing complex key structures while maintaining fast access patterns:

```rust
// For serialization - simple Vec
let serializable_data: Vec<Item> = items.into_iter().collect();

// For runtime - efficient HashMap
let lookup_map: HashMap<ItemId, Item> = 
    serializable_data.into_iter()
                    .map(|item| (item.id, item))
                    .collect();
```

When implementing caches, consider using reference-based APIs like `entry_ref` from hashbrown to avoid unnecessary cloning:

```rust
use hashbrown::HashMap;

// Avoids cloning the key for lookup
map.entry_ref(key_reference).or_insert_with(|| create_value());
```

Document your data structure choices to explain performance tradeoffs, especially when choosing specialized structures over standard library alternatives.