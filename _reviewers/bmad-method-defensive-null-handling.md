---
title: Defensive Null Handling
description: When values are optional (undefined/null), external data can be malformed,
  or runtime internals may not exist, code should *guard first* and choose safe, backward-compatible
  defaults instead of relying on truthiness.
repository: bmad-code-org/bmad-method
label: Null Handling
language: JavaScript
comments_count: 4
repository_stars: 51859
---

When values are optional (undefined/null), external data can be malformed, or runtime internals may not exist, code should *guard first* and choose safe, backward-compatible defaults instead of relying on truthiness.

Apply this standard:
- Feature-detect optional/internals and no-op when unavailable (avoid calling missing methods).
- Validate parsed/unknown data shapes explicitly: check for `null`, confirm `typeof === 'object'`, and also guard against arrays via `Array.isArray(...)`.
- For optional boolean-like flags, preserve backward compatibility by using explicit comparisons (e.g., treat “missing” as success, only fail when the field is explicitly `false`).
- If you must use sentinels/defaults, do it consistently (e.g., `id || ''`) and ensure downstream logic understands the sentinel.

Example pattern:
```js
function safeTabHandler(prompt) {
  const clear = prompt?._clearUserInput;
  const set = prompt?._setUserInput;
  if (typeof clear !== 'function' || typeof set !== 'function') return; // no-op
  clear();
  set(/* ... */);
}

function validateParsed(parsed) {
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    return { ok: false, reason: 'module.yaml must be a non-array object' };
  }
  return { ok: true };
}

function interpretSuccess(handlerResult) {
  // Missing `success` should remain backward compatible (default true)
  return handlerResult?.success !== false;
}
```

This prevents null reference errors, avoids crashes on malformed input, and keeps behavior stable when optional fields are introduced or absent.