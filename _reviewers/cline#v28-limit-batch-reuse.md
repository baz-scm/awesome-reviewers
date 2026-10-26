---
title: Limit, Batch, Reuse
description: When implementing performance-sensitive code, ensure external/expensive
  work is (1) bounded in scope, (2) batched across many items, and (3) never duplicated—compute
  once and reuse results.
repository: cline/cline#v28
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 70892
---

When implementing performance-sensitive code, ensure external/expensive work is (1) bounded in scope, (2) batched across many items, and (3) never duplicated—compute once and reuse results.

How to apply:
- Bound remote queries: don’t enumerate all remote branches/heads when you only need one (e.g., default/upstream). Prefer local remote-tracking refs or an explicit branch target.
- Batch per-item subprocess calls: replace “one process per file/item” with a single batch operation where possible (e.g., `git ... --batch`).
- Deduplicate expensive reads with side effects: if you call a function that performs clipboard/IO/network work, store its output and reuse it for both user-facing messages and telemetry.

Example (dedupe expensive terminal capture):
```ts
// BAD: calls IO twice
telemetryService.captureTerminalOutputFailure(...);
await returnCurrentTerminalContents();

// GOOD: capture once, reuse
const terminalSnapshot = await getLatestTerminalOutput();
const fallbackMsg = makeFallbackMessage(terminalSnapshot);
emitFallback(fallbackMsg);
telemetryService.captureTerminalOutputFailureReasoned(terminalSnapshot);
```

Example (batch git blob reads):
```ts
// BAD: spawns git per untracked file
await Promise.all(oids.map(oid => execGit(['show', `${ref}:${path}`])));

// GOOD: one batch process
const pending = execFile('git', ['-C', cwd, 'cat-file', '--batch'], { encoding: 'buffer' });
pending.child.stdin?.end([...new Set(oids)].join('\n') + '\n');
const { stdout } = await pending;
// parse stdout and build result map
```

Example (bound remote enumeration):
```ts
// BAD: ls-remote --heads <remote> (all heads)
const allHeads = await git(root, ['ls-remote', '--heads', remote]);

// GOOD: restrict to the branch you actually need (e.g., upstream/default)
const upstreamBranch = await getDefaultBranch(remote);
const headSha = await git(root, ['ls-remote', '--heads', remote, upstreamBranch]);
```