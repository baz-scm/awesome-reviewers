---
title: Naming consistency and compatibility
description: 'When changing names (identifiers, event naming schemes, exported types/APIs),
  follow a “normalize, verify, and preserve” rule:


  1) Normalize naming at the boundary'
repository: facebook/react#b5
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251886
---

When changing names (identifiers, event naming schemes, exported types/APIs), follow a “normalize, verify, and preserve” rule:

1) Normalize naming at the boundary
- Prefer fixing the naming once where the data enters the system rather than duplicating conversions/checks everywhere.
- If the platform provides `topPress`-style names, strip/normalize `top` at the dispatch boundary so downstream logic consistently uses `press`.

2) Verify renames are complete (avoid silent fallbacks)
- If you rename a prop/identifier, run a repo-wide search for the old spelling before merge.
- Don’t rely on defaults that can mask missing/incorrect names (e.g., `prop || default`).

3) Treat exported/semi-public names as API
- Changing names of exported or semi-public types (Flow/DT/TS externals) can be breaking even if not “exported” in code.
- Follow existing naming conventions; when transitioning, preserve backward compatibility via explicit aliases.

4) Follow established naming patterns/suffix rules
- If the codebase uses suffix conventions to distinguish render/static flags or similar categories, match them unless there’s an intentional, documented exception.

Example (API rename with alias for compatibility):
```js
// New name
export { Activity };
// Back-compat alias
export { Activity as unstable_Activity };
```

Example (rename verification before merge):
- After renaming `expectedEnviromentName` → `expectedEnvironmentName`, ensure the old spelling no longer exists:
  - `git grep -n expectedEnviromentName`

Checklist for PRs that touch names:
- [ ] Is the naming normalized once at the boundary (no repeated ad-hoc conversions)?
- [ ] Are all old spellings/identifiers removed or intentionally aliased?
- [ ] Were repo-wide searches run to confirm no lingering misspellings?
- [ ] Are exported/semi-public names preserved via existing conventions and explicit aliases/exports?
- [ ] Are suffix/pattern conventions maintained where they encode semantics? 