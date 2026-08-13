---
title: Preserve and Structure Failures
description: When errors occur—especially in multi-step operations—avoid accidental
  data loss and avoid “leaking” raw failures. Instead, preserve rollback artifacts
  and convert errors into documented, structured outcomes.
repository: bmad-code-org/bmad-method
label: Error Handling
language: Other
comments_count: 2
repository_stars: 51859
---

When errors occur—especially in multi-step operations—avoid accidental data loss and avoid “leaking” raw failures. Instead, preserve rollback artifacts and convert errors into documented, structured outcomes.

Apply this as two rules:
1) Recovery-first failure handling
- Don’t let broad/outer catch blocks delete rollback state.
- If a swap/replace fails, keep the previous install (or a backup sibling) so a failed operation can be manually or automatically rolled back.
- Emit a clear recovery hint (e.g., the preserved backup path) instead of failing silently.

Example pattern (rollback-safe):
```js
async function atomicSwapDir(stagedDir, targetDir) {
  const parent = path.dirname(targetDir);
  await fsp.mkdir(parent, { recursive: true });
  const suffix = crypto.randomBytes(6).toString('hex');
  const sibling = path.join(parent, `.${path.basename(targetDir)}.tmp-${suffix}`);
  const backup  = path.join(parent, `.${path.basename(targetDir)}.old-${suffix}`);

  try {
    await fsp.rename(stagedDir, sibling);
    const hadTarget = await fsp.stat(targetDir).then(() => true).catch(() => false);
    if (hadTarget) await fsp.rename(targetDir, backup);
    await fsp.rename(sibling, targetDir);
    if (hadTarget) await fsp.rm(backup, { recursive: true, force: true });
  } catch (e) {
    await fsp.rm(sibling, { recursive: true, force: true });
    // IMPORTANT: do NOT delete backup in the outer catch.
    // Preserve backup for recovery; optionally print its path to stderr.
    // console.error(`Swap failed; preserved backup at: ${backup}`);
    throw e;
  }
}
```

2) Structured, documented CLI outcomes
- Validate flags/arguments early; fail fast on unknown flags and missing required values.
- Map outcomes to consistent, documented exit codes.
- Treat `--help`/`-h` as success (exit 0).
- Treat incomplete/incorrect invocations as usage errors (e.g., `EXIT.USAGE`).

This combination prevents both worst-case outcomes: irrecoverable state loss and confusing/undocumented runtime failures.