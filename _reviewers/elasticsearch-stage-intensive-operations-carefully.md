---
title: Stage intensive operations carefully
description: When implementing operations that consume significant system resources
  (CPU, memory, I/O), introduce changes gradually while monitoring performance. This
  prevents cascading performance issues that can degrade the entire system.
repository: elastic/elasticsearch
label: Performance Optimization
language: Markdown
comments_count: 3
repository_stars: 73104
---

When implementing operations that consume significant system resources (CPU, memory, I/O), introduce changes gradually while monitoring performance. This prevents cascading performance issues that can degrade the entire system.

For example:
1. When modifying configuration parameters that trigger resource-intensive tasks (like decreasing `min_age` in Elasticsearch ILM policies), consider how many tasks might execute simultaneously
2. For threadpool size adjustments (like `thread_pool.force_merge.size`), increase gradually while monitoring system metrics
3. Consider where operations execute and potential trade-offs - operations on high-performance nodes may complete faster but could impact critical workflows like data ingestion

This approach helps maintain system stability while optimizing resource-intensive operations.
