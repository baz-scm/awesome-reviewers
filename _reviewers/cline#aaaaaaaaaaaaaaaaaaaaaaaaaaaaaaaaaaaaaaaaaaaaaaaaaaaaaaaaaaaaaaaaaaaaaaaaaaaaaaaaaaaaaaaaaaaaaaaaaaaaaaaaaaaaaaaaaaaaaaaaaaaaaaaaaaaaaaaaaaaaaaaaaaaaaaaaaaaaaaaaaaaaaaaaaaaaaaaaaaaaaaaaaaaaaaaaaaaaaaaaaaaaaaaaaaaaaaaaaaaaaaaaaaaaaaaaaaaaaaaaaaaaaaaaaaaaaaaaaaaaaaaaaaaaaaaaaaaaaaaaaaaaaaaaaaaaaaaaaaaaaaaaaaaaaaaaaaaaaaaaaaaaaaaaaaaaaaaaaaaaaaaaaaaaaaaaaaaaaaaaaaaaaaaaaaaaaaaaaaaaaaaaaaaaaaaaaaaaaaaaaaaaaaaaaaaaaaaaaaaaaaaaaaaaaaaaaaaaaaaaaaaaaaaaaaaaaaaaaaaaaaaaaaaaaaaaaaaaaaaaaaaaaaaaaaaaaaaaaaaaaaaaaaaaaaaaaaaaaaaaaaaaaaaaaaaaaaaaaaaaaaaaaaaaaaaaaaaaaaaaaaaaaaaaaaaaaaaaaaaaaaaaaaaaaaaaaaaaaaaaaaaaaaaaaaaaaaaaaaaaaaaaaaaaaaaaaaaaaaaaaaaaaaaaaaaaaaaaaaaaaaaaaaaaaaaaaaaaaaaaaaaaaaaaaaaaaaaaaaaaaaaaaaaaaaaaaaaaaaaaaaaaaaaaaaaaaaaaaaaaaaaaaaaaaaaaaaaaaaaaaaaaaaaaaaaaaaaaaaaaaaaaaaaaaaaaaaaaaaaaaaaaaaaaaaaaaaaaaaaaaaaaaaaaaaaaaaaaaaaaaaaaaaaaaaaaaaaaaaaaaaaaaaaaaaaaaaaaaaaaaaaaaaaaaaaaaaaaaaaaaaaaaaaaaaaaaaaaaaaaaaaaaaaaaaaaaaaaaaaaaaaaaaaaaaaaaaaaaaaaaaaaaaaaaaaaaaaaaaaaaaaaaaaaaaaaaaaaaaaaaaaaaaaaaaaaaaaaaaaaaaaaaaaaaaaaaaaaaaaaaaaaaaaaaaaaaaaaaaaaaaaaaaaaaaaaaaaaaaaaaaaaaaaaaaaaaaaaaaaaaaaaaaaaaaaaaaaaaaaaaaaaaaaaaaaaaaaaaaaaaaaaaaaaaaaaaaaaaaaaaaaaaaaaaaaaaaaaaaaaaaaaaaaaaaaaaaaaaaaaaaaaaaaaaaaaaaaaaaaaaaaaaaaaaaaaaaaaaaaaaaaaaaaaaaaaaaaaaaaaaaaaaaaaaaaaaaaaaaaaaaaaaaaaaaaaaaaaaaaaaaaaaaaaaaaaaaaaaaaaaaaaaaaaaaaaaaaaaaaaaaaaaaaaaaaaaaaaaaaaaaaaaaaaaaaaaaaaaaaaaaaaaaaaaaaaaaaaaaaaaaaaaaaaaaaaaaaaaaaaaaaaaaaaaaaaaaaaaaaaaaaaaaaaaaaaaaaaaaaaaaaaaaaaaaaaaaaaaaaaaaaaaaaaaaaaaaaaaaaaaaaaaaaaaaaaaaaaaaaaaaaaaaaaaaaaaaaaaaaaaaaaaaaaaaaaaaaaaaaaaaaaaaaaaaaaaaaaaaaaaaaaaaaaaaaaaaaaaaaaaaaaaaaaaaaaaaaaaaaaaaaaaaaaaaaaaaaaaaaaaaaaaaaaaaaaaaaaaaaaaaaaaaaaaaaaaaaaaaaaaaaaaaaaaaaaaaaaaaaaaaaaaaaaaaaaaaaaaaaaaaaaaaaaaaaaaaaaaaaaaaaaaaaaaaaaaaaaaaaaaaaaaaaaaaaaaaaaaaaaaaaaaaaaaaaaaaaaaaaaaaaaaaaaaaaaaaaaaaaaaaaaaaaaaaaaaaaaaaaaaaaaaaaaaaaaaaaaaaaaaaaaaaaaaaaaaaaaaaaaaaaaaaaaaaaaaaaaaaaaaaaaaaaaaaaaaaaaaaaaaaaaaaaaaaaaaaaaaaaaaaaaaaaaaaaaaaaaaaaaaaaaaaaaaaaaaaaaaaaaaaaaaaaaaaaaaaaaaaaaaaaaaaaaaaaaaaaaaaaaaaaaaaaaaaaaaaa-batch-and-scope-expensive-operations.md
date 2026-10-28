---
title: Batch and scope expensive operations
description: When an operation (subprocess spawn, network fetch, filesystem walk,
  clipboard round-trip, cache warm-up, etc.) is repeated once per item in a collection
  or once per poll/call, check whether it can instead be batched into a single call,
  scoped to only the data that actually changed, or reused from a result you already
  computed. Unbounded per-item or...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70973
---

When an operation (subprocess spawn, network fetch, filesystem walk, clipboard round-trip, cache warm-up, etc.) is repeated once per item in a collection or once per poll/call, check whether it can instead be batched into a single call, scoped to only the data that actually changed, or reused from a result you already computed. Unbounded per-item or per-poll costs scale badly and can exhaust system resources (e.g. spawning thousands of git processes for thousands of untracked files) or silently duplicate expensive side effects (e.g. running a full clipboard-capture round-trip twice to produce two values that should be the same).

Guidelines:
- Prefer one batched call over N per-item calls. For example, replace N `git show <ref>:<path>` spawns with a single `git cat-file --batch` call fed all the object IDs at once.
- Scale cost with the size of the actual change, not the size of the whole dataset. Replacing a full `git ls-tree -r` of an entire tree with `git diff --raw` against only the changed paths turns an O(repo size) operation into O(changes).
- Avoid re-fetching or re-computing a value you already have. If a helper function already produces a result internally (e.g. `getLatestTerminalOutput()`), have it return that result and reuse it at the call site instead of invoking the expensive operation again for telemetry, logging, or a second consumer.
- Guard periodic/frequently-polled logic (e.g. a 5s UI poll) so repeat invocations don't re-trigger an expensive initialization; run it once per distinct target (e.g. once per workspace) and let it reload only when something material actually changes.
- Where an unavoidable per-item cost remains (e.g. reading a bounded set of rules files), cap the item count and size explicitly and document the resulting worst case so it stays verifiable.
- Validate cap/timeout choices against real-world data (telemetry, production repro, or targeted benchmarks) rather than guesswork, and record the data that justified the chosen bound.

Example — batch instead of per-item spawn:
```ts
// Before: one git process per blob
const contents = await Promise.all(paths.map(p => runGit(cwd, ["show", `${ref}:${p}`])));

// After: one batched process for all blobs
const input = [...new Set(oids)].join("\n");
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], { input });
```

Example — reuse instead of duplicate fetch:
```ts
// Before: fetched twice, can diverge
await returnCurrentTerminalContents()
const snapshot = await getLatestTerminalOutput() // duplicate expensive round-trip

// After: fetch once, reuse everywhere
const snapshot = await returnCurrentTerminalContents() // now returns the snapshot it fetched
```
</description>
