---
title: Stable Interface Normalization
description: Define and enforce normalization rules for all user/client-facing inputs
  (CLI flags, request fields, option keys) so matching behavior is consistent with
  the documented interface contract—then harden implementations against dependency/API
  drift.
repository: bmad-code-org/bmad-method
label: API
language: JavaScript
comments_count: 2
repository_stars: 51859
---

Define and enforce normalization rules for all user/client-facing inputs (CLI flags, request fields, option keys) so matching behavior is consistent with the documented interface contract—then harden implementations against dependency/API drift.

Apply:
- Normalize before matching: if an identifier is treated case-insensitively by contract, lowercase/trim (or otherwise normalize) *both* the user input and the candidate values.
- Add tests covering common variations (e.g., uppercase vs lowercase).
- If implementing behavior requires using private/unstable library internals, mitigate risk:
  - isolate the workaround in one clearly-marked section,
  - pin the dependency version,
  - document the expected fallback (graceful degradation) so the UI/API doesn’t crash or corrupt data.

Example (case-insensitive option matching):
```js
async function formatOptionsList(moduleCode, discovered) {
  const needle = moduleCode ? moduleCode.toLowerCase() : null;
  const filtered = needle
    ? discovered.filter((d) => d.code.toLowerCase() === needle)
    : discovered;
  // ...render filtered results
}
```

Example (safe, isolated workaround pattern for UI behavior):
```js
// Mark clearly: workaround for library private behavior; pin dependency version.
const originalIsActionKey = prompt._isActionKey.bind(prompt);
prompt._isActionKey = function (char, key) {
  if (key && key.name === 'space') return true; // expected selection behavior
  return originalIsActionKey(char, key);
};
// Add a SPACE handler only if needed; ensure no crashes and acceptable fallback.
```