---
title: Validate and normalize untrusted paths
description: 'When accepting file paths or names from untrusted input (e.g., prompts,
  API payloads) that will be written to disk or used to run external tools, enforce
  strict allow-list validation before use: reject absolute paths (both POSIX and Windows
  styles), path traversal segments, control characters, reserved device names (CON,
  PRN, AUX, NUL, COMn, LPTn), trailing...'
repository: promptfoo/promptfoo
label: Security
language: Other
comments_count: 1
repository_stars: 26565
---

When accepting file paths or names from untrusted input (e.g., prompts, API payloads) that will be written to disk or used to run external tools, enforce strict allow-list validation before use: reject absolute paths (both POSIX and Windows styles), path traversal segments, control characters, reserved device names (CON, PRN, AUX, NUL, COMn, LPTn), trailing dots/spaces, unpaired surrogates, and references to sensitive directories (e.g., .git, .env). In addition, normalize each path segment consistently (Unicode NFC normalization plus case folding) before using it as a deduplication key or writing it to disk, since filesystems can be case-insensitive and/or Unicode-normalizing. Without this normalization, visually distinct inputs (e.g., Unicode confusables like 'σ' vs final-sigma 'ς', or differently-cased names) can collide unexpectedly on disk, causing unintended overwrites, cache poisoning, or validation bypass. Example:

```js
// Validate
if (path.posix.isAbsolute(name) || path.win32.isAbsolute(name) || /\.\.|[\u0000-\u001f<>:"|?*]/.test(name)) {
  throw new Error(`Invalid path: ${name}`);
}
// Normalize for collision-safe keys
const target = name.normalize('NFC').toLowerCase();
if (seen.has(target)) {
  throw new Error(`Duplicate path after normalization: ${name}`);
}
```

Apply this pattern whenever untrusted names are mapped to filesystem resources, ensuring both strict rejection of dangerous inputs and normalization that matches the actual OS/filesystem semantics.