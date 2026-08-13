---
title: Strict Input Validation
description: Always validate and constrain any user-controlled or data-driven strings
  (IDs, slugs, CLI flags, manifest/CSV fields) before using them to build paths, filenames,
  or subprocess commands, and apply defense-in-depth against common classes of attacks.
repository: bmad-code-org/bmad-method
label: Security
language: JavaScript
comments_count: 6
repository_stars: 51859
---

Always validate and constrain any user-controlled or data-driven strings (IDs, slugs, CLI flags, manifest/CSV fields) before using them to build paths, filenames, or subprocess commands, and apply defense-in-depth against common classes of attacks.

Practical rules:
- Prefer allowlists: validate identifiers with tight regexes (e.g., lowercase slug patterns). Reject anything that doesn’t match.
- Block traversal/path escapes: for anything used as a filename/path segment, reject values containing `..`, path separators (`/` or `\`), or unexpected whitespace.
- Avoid shell interpolation: when spawning processes, use APIs that take argument arrays (e.g., `execFileSync`) instead of building a shell command string.
- Protect object maps: when constructing objects from dynamic keys, use `Object.create(null)` and reject dangerous keys like `__proto__`, `prototype`, and `constructor`.
- Keep validator strictness consistent with runtime consumers: don’t broaden accepted input in validation (e.g., don’t implicitly `.trim()` a field if runtime parsing does not).

Example pattern (safe subprocess + strict slug + path-segment guard):
```js
const path = require('node:path');
const fs = require('node:fs');
const { execFileSync } = require('node:child_process');

const SLUG_RE = /^[a-z0-9][a-z0-9-]*$/;
function assertSafeSlug(slug) {
  if (!SLUG_RE.test(slug)) throw new Error(`Invalid slug: ${slug}`);
}

function zipBundle({ bundlesDir, distDir, slug }) {
  assertSafeSlug(slug);
  const srcDir = path.join(bundlesDir, slug);
  const outZip = path.join(distDir, `${slug}.zip`);
  fs.mkdirSync(distDir, { recursive: true });

  // No shell interpolation
  execFileSync('zip', ['-r', '-X', '-q', outZip, slug, '-x', '*.DS_Store'], {
    cwd: bundlesDir,
    stdio: 'inherit',
  });
}
```

Apply this check any time code does one of these: writes files, reads files by derived paths, constructs regexes from inputs, or spawns external commands using derived arguments.