---
title: prefer lazy computation
description: Avoid precomputing expensive operations when they may not be needed,
  especially for large datasets. Instead, compute values on-demand when they are actually
  required. This prevents unnecessary work and improves performance for scenarios
  where only a subset of computed values will be used.
repository: browserbase/stagehand
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 16443
---

Avoid precomputing expensive operations when they may not be needed, especially for large datasets. Instead, compute values on-demand when they are actually required. This prevents unnecessary work and improves performance for scenarios where only a subset of computed values will be used.

When designing algorithms, resist the temptation to use oversimplified heuristics or "quick fixes" that may create edge cases. Take time to implement proper solutions rather than relying on magic numbers or hacky workarounds.

Example of the problem:
```typescript
// Bad: Precomputing XPaths for all nodes
for (const node of nodes) {
  if (node.backendDOMNodeId !== undefined) {
    const xpath = await getXPathByResolvedObjectId(cdpClient, objectId);
    node.xpath = xpath; // May never be used
  }
}

// Good: Compute XPaths only when needed
async function getXPathForNode(node: AXNode): Promise<string> {
  if (!node.xpath && node.backendDOMNodeId) {
    node.xpath = await getXPathByResolvedObjectId(cdpClient, node.backendDOMNodeId);
  }
  return node.xpath;
}
```

This approach scales better with large datasets and avoids wasted computation cycles on unused data.