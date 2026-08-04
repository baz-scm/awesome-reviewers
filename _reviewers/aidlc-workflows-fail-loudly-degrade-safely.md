---
title: Fail Loudly, Degrade Safely
description: In session/install hooks, never hide failures. Avoid OS/tool-specific
  command forms and exit-code-dependent fallbacks, and when an error occurs either
  (1) stop with a clear message or (2) degrade gracefully while recording structured
  diagnostics so `--doctor`/health checks can surface what broke.
repository: awslabs/aidlc-workflows
label: Error Handling
language: Shell
comments_count: 3
repository_stars: 3849
---

In session/install hooks, never hide failures. Avoid OS/tool-specific command forms and exit-code-dependent fallbacks, and when an error occurs either (1) stop with a clear message or (2) degrade gracefully while recording structured diagnostics so `--doctor`/health checks can surface what broke.

Apply these standards:
- **No silent suppression:** Don’t use `2>/dev/null || true` around critical compose/compile steps. If you must continue, catch exceptions and record a “drop”/health entry.
- **Log actionable context:** When recording failures, include which step failed, the failing input (path/file), and the error message/stack.
- **Make behavior portable/deterministic:** Don’t rely on GNU-only flags (e.g., `sed -i` form) or `cp -n` exit semantics as a branching signal. Prefer explicit checks like `existsSync(dest)` / `if [ -f "$target" ]`.
- **Keep idempotence without overwrites:** For “no-clobber” copy, skip existing destinations deterministically rather than using fallback copies that may overwrite.

Example (bun/TS compose layer):
```ts
import fs from "node:fs";

function recordDrop(step: string, err: unknown) {
  // write to aidlc/.aidlc-hooks-health/... (implementation omitted)
  console.error(`[compose-drop] ${step}:`, err);
}

async function copyNoClobber(srcRoot: string, dstRoot: string) {
  for (const entry of fs.readdirSync(srcRoot, { withFileTypes: true })) {
    const src = `${srcRoot}/${entry.name}`;
    const dst = `${dstRoot}/${entry.name}`;
    if (fs.existsSync(dst)) continue; // deterministic no-clobber
    if (entry.isDirectory()) {
      fs.mkdirSync(dst, { recursive: true });
      await copyNoClobber(src, dst);
    } else {
      fs.copyFileSync(src, dst);
    }
  }
}

export async function runCompose() {
  try {
    await copyNoClobber("$PLUGIN_ROOT/stages", "$HARNESS_DIR/aidlc-common/stages");
    // ...merge contributions + compile graph
  } catch (err) {
    recordDrop("plugin-compose", err);
    // degrade safely: don’t silently succeed
  }
}
```
This ensures macOS/Windows differences don’t break composition invisibly, and users/devs can quickly identify what failed and why.