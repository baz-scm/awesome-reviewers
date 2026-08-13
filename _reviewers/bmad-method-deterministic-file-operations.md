---
title: Deterministic File Operations
description: 'When implementing concurrent or bulk filesystem operations, ensure deterministic
  execution and atomicity: avoid async wrappers/behavior that introduce retry queues
  or event-loop interleaving that can reorder unlinks/overwrites.'
repository: bmad-code-org/bmad-method
label: Concurrency
language: JavaScript
comments_count: 2
repository_stars: 51859
---

When implementing concurrent or bulk filesystem operations, ensure deterministic execution and atomicity: avoid async wrappers/behavior that introduce retry queues or event-loop interleaving that can reorder unlinks/overwrites.

Practical rules:
- For bulk copy/move sequences where ordering matters, don’t rely on third-party async fs layers that defer retries via the event loop. If needed, implement the operation synchronously (but keep the exported API async-compatible) to eliminate interleaving.
- For replace/update flows, prefer a true atomic swap/rename that guarantees consistent replacement semantics; don’t add redundant “exists then remove” logic that is already covered, and don’t introduce new collision/guard behavior unless you’ve explicitly agreed it won’t break reinstall/update workflows.

Example pattern (deterministic copy under an async API):
```js
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');

function copyDirSync(src, dest, overwrite) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDirSync(srcPath, destPath, overwrite);
    else {
      if (!overwrite && fs.existsSync(destPath)) continue;
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

async function copy(src, dest, { overwrite = true } = {}) {
  const st = await fsp.stat(src);
  if (st.isDirectory()) {
    copyDirSync(src, dest, overwrite); // deterministic ordering
  } else {
    await fsp.mkdir(path.dirname(dest), { recursive: true });
    if (!overwrite) {
      try { await fsp.access(dest); return; } catch {}
    }
    fs.copyFileSync(src, dest);
  }
}
```