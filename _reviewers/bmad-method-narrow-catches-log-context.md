---
title: Narrow catches, log context
description: 'When handling errors, avoid two failure modes: (a) false-success/zero-signal
  outcomes and (b) silent data loss. Apply these rules consistently:


  1) Fail loudly when correctness is impossible'
repository: bmad-code-org/bmad-method
label: Error Handling
language: JavaScript
comments_count: 12
repository_stars: 51859
---

When handling errors, avoid two failure modes: (a) false-success/zero-signal outcomes and (b) silent data loss. Apply these rules consistently:

1) Fail loudly when correctness is impossible
- If the tool/install depends on an input that must exist/parse (e.g., required configs/manifests; or the scanned source directory), do not catch and return success/empty results.

2) Narrow try/catch scope to only the recoverable part
- Wrap only the read/parse that you intend to degrade. If you recover, log a warning with enough identifiers to locate the problem (file path, module/key, canonicalId/slug).
- Do not swallow exceptions in the subsequent “core” logic: let those errors surface.

3) Don’t swallow unrelated exceptions
- Catch only expected error codes (e.g., ENOENT/ENOTDIR for existence checks). Re-throw permission errors (EACCES) and everything else.

4) When using fallbacks/retries, preserve provenance
- If a primary method fails and a fallback is attempted, include both failure contexts in the final error (e.g., with AggregateError).

Example pattern (warn-and-degrade, but only for non-fatal parsing):
```js
async function seedFromSchema({ yes, configCollector, directory, prompts, fs, path, getSourcePath }) {
  if (!yes) return;

  try {
    const yaml = require('yaml');
    const schemaPath = path.join(getSourcePath('core-skills'), 'module.yaml');
    const coreSchema = yaml.parse(await fs.readFile(schemaPath, 'utf8')); // narrowed catch target

    // core seeding logic lives OUTSIDE the narrow catch scope
    const core = (configCollector.collectedConfig.core ||= {});
    // ... proceed with seeding; errors here should surface
  } catch (err) {
    prompts.log.warn(`Core schema unavailable; skipping backfill: ${err.message}`);
    // continue install; do not hide failures in later critical steps
  }
}
```

Use this checklist in review:
- Is there any scenario where we should “warn and continue” vs “fail fast”?
- Is the try/catch limited to the recoverable operation?
- Are we logging enough context to debug?
- Are we only swallowing expected errors (specific codes), and rethrowing others?
- If we fallback, do we preserve both error causes? 
