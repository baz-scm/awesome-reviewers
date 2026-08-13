---
title: Containment and Install Policy
description: 'For security-sensitive filesystem and dependency-install flows, treat
  any path/ref derived from CLI input or manifests as untrusted: (1) parse/validate
  it, and (2) strictly contain it to the intended root before any filesystem mutation
  (copy/swap/delete). Also, keep security posture consistent across equivalent install
  mechanisms.'
repository: bmad-code-org/bmad-method
label: Security
language: Other
comments_count: 4
repository_stars: 51859
---

For security-sensitive filesystem and dependency-install flows, treat any path/ref derived from CLI input or manifests as untrusted: (1) parse/validate it, and (2) strictly contain it to the intended root before any filesystem mutation (copy/swap/delete). Also, keep security posture consistent across equivalent install mechanisms.

Apply these standards:
- Path containment before mutation: Use the project’s existing containment helper (e.g., a `safePathInsideRoot`-style check) to reject `..`, absolute paths, and symlink/escape attempts. Perform the check both for directory targets (e.g., before `atomicSwapDir`) and for each per-file path from manifests before calling `fs.rm`/`fs.copy`/staging.
- Fail/skip safely: If a validated path check fails, throw `PATH_TRAVERSAL` for “should never escape” cases, or skip with a clear warning when removing files discovered in manifests.
- Npm install security consistency: If you need to harden dependency installs (e.g., adding/removing `--ignore-scripts`), implement it as a deliberate, shared policy across all relevant install paths (installer + skills). Avoid “one-off” flag changes that create inconsistent security behavior.

Minimal example (pattern):
```js
import { safePathInsideRoot } from './fs-safe.mjs';

function rmManifestPath(bmadDir, manifestRelPath) {
  const abs = safePathInsideRoot(bmadDir, path.join(bmadDir, manifestRelPath));
  return fs.rm(abs, { force: true });
}

// Before swapping/copying an install target:
const safeTargetDir = safePathInsideRoot(bmadDir, targetDir);
await atomicSwapDir(safeTargetDir, stagedDir);
```