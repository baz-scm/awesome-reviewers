---
title: Single Source Config
description: Ensure configuration is maintainable and compatible by (1) using a single
  authoritative field and deriving dependent values at runtime, and (2) pinning configuration-relevant
  dependency versions when they enforce runtime compatibility (e.g., CommonJS vs ESM)
  until you intentionally migrate.
repository: bmad-code-org/bmad-method
label: Configurations
language: Json
comments_count: 2
repository_stars: 51859
---

Ensure configuration is maintainable and compatible by (1) using a single authoritative field and deriving dependent values at runtime, and (2) pinning configuration-relevant dependency versions when they enforce runtime compatibility (e.g., CommonJS vs ESM) until you intentionally migrate.

Apply it like this:
- Remove duplicated config keys that must be updated together.
- Compute derived URLs/values from the canonical config (e.g., `releaseTag`).
- When a dependency version affects module/runtime behavior, keep it pinned and only bump after validating the compatibility impact.

Example patterns:
```js
// Derive dependent config from a single authoritative field
const { releaseTag } = bundlesJson;
function bundleUrl(slug) {
  return `https://github.com/bmad-code-org/BMAD-METHOD/releases/download/${releaseTag}/${slug}.zip`;
}
```
```json
// Pin versions when runtime compatibility matters
{
  "dependencies": {
    "ora": "^5.4.1"
  }
}
```