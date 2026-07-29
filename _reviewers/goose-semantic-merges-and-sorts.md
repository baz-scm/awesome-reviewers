---
title: Semantic merges and sorts
description: When implementing algorithms that merge incremental updates and compute
  ordering (grouping/sorting), ensure the algorithm matches the *producer semantics*
  and uses *semantically correct keys*—don’t rely on heuristic fixes.
repository: aaif-goose/goose
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 51876
---

When implementing algorithms that merge incremental updates and compute ordering (grouping/sorting), ensure the algorithm matches the *producer semantics* and uses *semantically correct keys*—don’t rely on heuristic fixes.

Apply these rules:
1) Incremental merge semantics: if the upstream emits append-only deltas, merge with append (e.g., `+=`). If chunks are cumulative, only then use overwrites or dedup logic.
2) Sorting/grouping keys: sort by the timestamp that represents the *meaningful event* (e.g., “last message activity”), not by generic `updatedAt` that may change for renames/metadata-only updates.
3) Live/remote dependencies: if the input set is built via remote discovery, bound per-provider latency and fall back to a stable cache to prevent the whole computation from stalling.

Example patterns (adapted):
```ts
// 1) Append-only delta merge (don’t use dedup/overlap heuristics)
function mergeTextDelta(existing: string, incomingChunk: string) {
  return existing + incomingChunk;
}

// 2) Semantically correct sort key
const tA = new Date(a.lastMessageAt ?? a.updatedAt).getTime();
const tB = new Date(b.lastMessageAt ?? b.updatedAt).getTime();
projectSessions.sort((a, b) => tB - tA);

// 3) Bounded live discovery with fallback
async function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`timed out after ${ms}ms`)), ms);
    p.then(v => { clearTimeout(timer); resolve(v); }, e => { clearTimeout(timer); reject(e); });
  });
}

async function getModelsWithFallback(live: () => Promise<string[]>, cache: string[], ms = 4000) {
  try {
    return await withTimeout(live(), ms);
  } catch {
    return cache;
  }
}
```
This prevents subtle UI/state bugs caused by incorrect merge assumptions, wrong sort keys, and unbounded remote computation.