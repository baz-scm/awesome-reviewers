---
title: Avoid hidden performance costs
description: When designing APIs that interact with remote services, be cautious about
  implementing convenience features that may introduce significant hidden performance
  costs. Collection operations like slicing, negative indexing, or operations that
  process all items can be unexpectedly expensive when they require fetching large
  amounts of data.
repository: boto/boto3
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 9417
---

When designing APIs that interact with remote services, be cautious about implementing convenience features that may introduce significant hidden performance costs. Collection operations like slicing, negative indexing, or operations that process all items can be unexpectedly expensive when they require fetching large amounts of data.

Consider these strategies to optimize performance:

1. Use explicit parameters like `limit` to control resource fetching
2. Avoid creating resource instances for items that won't be used
3. When implementing potentially expensive operations, consider:
   - Disabling features that always require inefficient implementations (like negative indexing)
   - Making expensive operations explicit through separate methods
   - Documenting performance implications clearly

For example, instead of supporting negative indexing directly:

```python
# Potentially expensive - fetches all items to get the last one
last_item = collection[-1]

# Better - makes the expensive operation explicit
last_item = collection.to_list()[-1]  # User is aware of full collection materialization
# Or provide a direct method
last_item = collection.get_last()  # Could be optimized internally
```

This approach gives users control over performance tradeoffs and avoids surprising them with unexpectedly expensive operations.