---
title: Normalize Generated Output
description: When generating files/metadata, make output deterministic and cross-platform
  by normalizing both *paths* and *text line endings*, and by keeping shared formatting
  rules/filters centralized.
repository: bmad-code-org/bmad-method
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 51859
---

When generating files/metadata, make output deterministic and cross-platform by normalizing both *paths* and *text line endings*, and by keeping shared formatting rules/filters centralized.

**Rules**
1. **Normalize path separators** in generated strings used in manifests/CSVs/etc. (e.g., convert `path.sep` to `/`).
2. **Normalize line endings** when emitting text files (e.g., Markdown). Build strings with `\n`, then convert to `os.EOL` (or keep `\n` consistently if the consumer expects it).
3. **Centralize shared constants** used in generation/copy/patch logic (e.g., exclusion dir sets) so every site uses the same rule.
4. **Avoid redundant requires/imports**—use existing wrappers already in scope to reduce drift.

**Example**
```js
import os from 'node:os';
import path from 'node:path';

function normalizeForCsv(relativePath) {
  return relativePath.split(path.sep).join('/');
}

async function writeTextFileNormalized(fs, filePath, content) {
  // Build with explicit \n, then adapt to platform
  const platformContent = os.EOL === '\n' ? content : content.replace(/\r?\n/g, os.EOL);
  await fs.writeFile(filePath, platformContent, 'utf8');
}
```
