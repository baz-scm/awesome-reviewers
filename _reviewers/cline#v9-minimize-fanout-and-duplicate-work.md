---
title: Minimize Fanout And Duplicate Work
description: When code interacts with external systems (git, network, terminals, model
  streaming), avoid unnecessary work and wide fanout. This improves speed, reduces
  resource spikes, and prevents inconsistent results.
repository: cline/cline#v9
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70868
---

When code interacts with external systems (git, network, terminals, model streaming), avoid unnecessary work and wide fanout. This improves speed, reduces resource spikes, and prevents inconsistent results.

**Apply these rules:**
1. **Batch/fan-in external commands**: prefer one `git cat-file --batch` / single network call over per-file/per-item subprocesses.
2. **Scope preflight discovery**: don’t fetch all remote refs/heads/large histories just to show a preview; limit to the default/upstream branch or already-available local refs.
3. **Reuse captured data**: if you already fetched a snapshot (terminal output, parsed frame, computed preview), reuse it for telemetry and downstream logic—don’t re-run the capture.
4. **Align timeouts with actual “useful output” semantics**: for streaming, a “first chunk” timeout should only start when your code can observe the relevant output; gate `firstChunkMs` to explicit configuration or choose a safer default.

**Example (reuse snapshot instead of re-capturing):**
```ts
// Bad: capture twice
const ok = await returnCurrentTerminalContents();
telemetry.captureTerminalOutputFailure();

// Good: capture once and reuse
const snapshot = await returnCurrentTerminalContents();
telemetry.captureTerminalOutputFailure({ snapshot } );
```

**Example (batch git blob reads):**
```ts
// Bad: spawning git per file
await Promise.all(files.map(f => runGit(cwd, ['show', `${ref}:${f}`])));

// Good: list once, then batch contents via cat-file
const blobs = await runGit(cwd, ['ls-tree','-r','-l','-z', treeish]);
const contents = await execFile('git', ['-C', cwd,'cat-file','--batch']);
```

Use this as a quick checklist in PRs: *“Does this add extra subprocesses, extra network calls, or duplicate expensive captures? If so, can we batch, scope, and reuse?”*