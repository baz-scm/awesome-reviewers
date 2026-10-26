---
title: Validate Configuration Paths
description: When configuration affects filesystem locations or packaged artifacts,
  ensure it is (1) correct across supported environments and (2) aligned with the
  actual tooling behavior.
repository: cline/cline#v17
label: Configurations
language: Other
comments_count: 2
repository_stars: 70883
---

When configuration affects filesystem locations or packaged artifacts, ensure it is (1) correct across supported environments and (2) aligned with the actual tooling behavior.

**Path handling**
- Don’t rely on ambiguous shorthand without documenting/confirming resolution (e.g., what `~` becomes on Windows, and whether it maps to the expected user profile/profile type).
- If the runtime loads from user-specific directories, state the exact directories and how they are derived per OS.

**Packaging/ignore rules**
- Avoid duplicating ignore rules that the packaging tool already applies; duplicated rules are easy to make stale.
- Verify the effective packaged output (e.g., using the packaging tool’s listing/inspection commands) after changing `.vscodeignore`, scripts, or build filters.

**Example (clear, cross-platform path documentation)**
```md
Global plugins:      ~/.cline/plugins/
Project plugins:    ./.cline/plugins/
User plugins:       (resolved per OS)
- macOS/Linux:       ~/Documents/Cline/Plugins/
- Windows:          %USERPROFILE%/Documents/Cline/Plugins/
```

Apply this standard to docs and config whenever you introduce or modify environment-dependent paths (like plugin directories) or packaging filters (like `.vscodeignore` / copy scripts).