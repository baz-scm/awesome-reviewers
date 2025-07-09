---
title: Document connection transitions
description: 'When implementing systems that involve network connection state changes
  (such as during failovers, restarts, or component promotions), explicitly document
  and implement connection handling strategy for all affected components. '
repository: neondatabase/neon
label: Networking
language: Markdown
comments_count: 2
repository_stars: 19015
---

When implementing systems that involve network connection state changes (such as during failovers, restarts, or component promotions), explicitly document and implement connection handling strategy for all affected components. 

Key considerations:
1. Identify which component is responsible for terminating existing connections during transitions
2. Document the sequence of connection-related operations during state changes
3. Implement safeguards against stale reads from outdated connections
4. Consider connection invalidation mechanisms for proxies and clients

For example, when designing a compute promotion flow:
```
3.1. Terminate the primary compute. Starting from here, this is a critical section.
3.2. Send cache invalidation message to all proxies, notifying them that all new connections
     should request and wait for the new connection details.
3.3. Ensure proxies drop any existing connections to the old primary to prevent stale reads.
```

This approach prevents inconsistent state during transitions and makes connection handling behavior explicit rather than implicit, reducing the risk of connection-related bugs that can be difficult to diagnose in distributed systems.