---
title: Align naming across products
description: Maintain a single, consistent naming scheme for identifiers (fields,
  event names, config keys, and user-facing terminology) across all product surfaces.
repository: cline/cline#v22
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70886
---

Maintain a single, consistent naming scheme for identifiers (fields, event names, config keys, and user-facing terminology) across all product surfaces.

**Standard**
- **Parity first:** If two surfaces are supposed to represent the same concept (e.g., hook event payloads, config options), ensure the *field names and shapes* match.
- **Track mismatches:** For every naming mismatch discovered, file a bug so alignment work is not left as documentation-only fixes.
- **Deprecate, don’t fork:** If old names must change, keep legacy names working temporarily via an explicit mapping, and **deprecate** the old identifiers instead of silently diverging.
- **Document runtime truth:** Ensure docs use the same names/terminology as the code paths users will hit (especially when multiple builds/rollouts exist).

**Example (naming/shape alignment + deprecation)**
```jsonc
// Target aligned shape for hooks across products
{
  "hookName": "PreToolUse",
  "taskId": "conv-123",
  "workspaceRoots": ["/path/to/repo"],
  "toolCall": {                 // aligned field name
    "id": "call-456",
    "name": "read_files",
    "input": { "files": [{ "path": "src/index.ts" }] }
  }
}

// Temporary compatibility mapping (legacy)
// - read old shapes/keys (e.g., preToolUse.toolName / preToolUse.parameters)
// - map them internally to the aligned names
// - emit a deprecation warning and plan removal
```

Apply this to any naming surface: JSON fields, hook/event names, config keys, and the terms used in docs—so users don’t need to memorize per-product spelling differences or guess which variant their settings apply to.