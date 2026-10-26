---
title: Avoid duplicate expensive IO
description: 'When performance-sensitive code needs repo/network/terminal data, avoid
  wasted work: constrain the scope of what you fetch/enumerate, reuse snapshots already
  computed in the current call, and batch external commands so you don’t spawn/perform
  the same expensive operation repeatedly.'
repository: cline/cline#v22
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70886
---

When performance-sensitive code needs repo/network/terminal data, avoid wasted work: constrain the scope of what you fetch/enumerate, reuse snapshots already computed in the current call, and batch external commands so you don’t spawn/perform the same expensive operation repeatedly.

Apply this standard:
- Scope remote enumeration: don’t list every ref/head/commit “just to preview.” Prefer upstream/default branch only, local remote-tracking refs, or other narrowly-scoped queries.
- Reuse computed snapshots: if a function already captures terminal output, filesystem state, or a parsed git result, reuse that value for telemetry/success flags—don’t call the capture again.
- Batch external commands: replace per-file/per-item `git show`/process spawning with a single batched command (e.g., `git cat-file --batch`) and parse results once.
- Avoid duplicated preflights: if multiple layers read/validate the same repo, consolidate so the repo is effectively processed once (or ensure each layer’s checks are strictly additive and not repeating earlier I/O).

Example (reuse snapshot to avoid duplicate capture):
```ts
// Don’t do: capture() inside returnCurrentTerminalContents(), then call
// capture() again for telemetry.

const terminalSnapshot = await getLatestTerminalOutput();
const fallbackMessage = buildFallbackMessage(terminalSnapshot);
model.emit(fallbackMessage);
telemetry.captureSuccess({ snapshot: terminalSnapshot });
```

Example (batch git object reads):
```ts
const input = [...new Set(oids)].join("\n");
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], {
  encoding: "buffer",
});
// parse stdout once into oid -> content
```