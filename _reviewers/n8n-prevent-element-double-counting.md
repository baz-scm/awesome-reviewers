---
title: Prevent element double-counting
description: 'When working with graph structures, collections, or relationship mappings,
  ensure each element is processed exactly once to maintain algorithmic integrity.
  Implement proper tracking mechanisms to prevent duplicate counting or processing
  of elements, especially in scenarios involving:'
repository: n8n-io/n8n
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 122978
---

When working with graph structures, collections, or relationship mappings, ensure each element is processed exactly once to maintain algorithmic integrity. Implement proper tracking mechanisms to prevent duplicate counting or processing of elements, especially in scenarios involving:

1. Bi-directional relationships where an element might be both source and target
2. Self-referential connections or cycles
3. Multiple traversal paths that converge
4. Collection operations where uniqueness must be preserved

For example, instead of unconditionally adding items to collections:

```javascript
// Problematic: Elements may be added multiple times
this.runOrder.push(runKey);

// Better: Check before adding to prevent duplicates
if (!this.runOrder.includes(runKey)) this.runOrder.push(runKey);
```

When counting connections in graphs, track which connections have been counted:

```javascript
// Problematic: May count self-loops twice
function countNodeConnections(nodeId, connections) {
  let count = 0;
  
  // Count outgoing connections
  if (connections[nodeId]) {
    // Count outgoing logic...
    count += outgoingCount;
  }
  
  // Count incoming connections (may include duplicates with self-loops)
  for (const [sourceNodeId, nodeConnections] of Object.entries(connections)) {
    // Count incoming logic that doesn't account for sourceNodeId === nodeId
    count += incomingCount;
  }
  
  return count;
}

// Better: Use a Set to track unique connections
function countNodeConnections(nodeId, connections) {
  const countedConnections = new Set();
  let count = 0;
  
  // Add logic to track unique connection IDs to prevent double-counting
  // Only increment count for connections not already in the Set
  
  return count;
}
```

This approach prevents algorithmic errors that affect calculations, state management, and the correctness of graph operations.