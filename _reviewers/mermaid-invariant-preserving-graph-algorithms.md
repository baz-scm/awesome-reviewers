---
title: Invariant-Preserving Graph Algorithms
description: 'When a graph/geometry algorithm is used recursively (or downstream computations
  depend on its shape/metrics), don’t patch symptoms. Preserve invariants end-to-end:'
repository: mermaid-js/mermaid
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 87952
---

When a graph/geometry algorithm is used recursively (or downstream computations depend on its shape/metrics), don’t patch symptoms. Preserve invariants end-to-end:

- Fix the algorithmic root cause: if label/point alignment breaks due to path generation (e.g., curve smoothing not passing through control points), change the path/curve strategy (e.g., use ELK-style “nice corners”/corner treatment) so label positioning assumptions remain true.
- Propagate only safe configuration: when setting subgraph graph params, copy only the layout invariants you intend (e.g., ranksep/nodesep). Avoid copying unrelated spacing fields that can shift layout (e.g., marginy).
- Use robust data structures for algorithm state: prefer `Map` over plain objects for wrapper/global state (descendants/parents/cluster DB) to avoid key collisions and make updates predictable.

Example (subgraph config propagation):
```js
// In recursive render for subgraphs
const { ranksep, nodesep } = graph.graph();
node.graph.setGraph({
  ...node.graph.graph(),
  ranksep,
  nodesep,
});
```

Example (wrapper state as Map):
```js
export let clusterDb = new Map();
let descendants = new Map();
let parents = new Map();

export const clear = () => {
  clusterDb = new Map();
  descendants = new Map();
  parents = new Map();
};
```