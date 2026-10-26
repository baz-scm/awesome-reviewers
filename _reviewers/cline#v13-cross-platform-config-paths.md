---
title: Cross-platform config paths
description: 'When documenting or implementing configuration/plugin/cache locations,
  treat them as cross-platform and security-sensitive:


  - Use explicit, OS-appropriate path examples (especially Windows). Avoid ambiguous
  shorthand (like `~`) unless you’ve verified it expands correctly on Windows (e.g.,
  to the user profile) and confirm behavior for supported profile...'
repository: cline/cline#v13
label: Configurations
language: Other
comments_count: 2
repository_stars: 70874
---

When documenting or implementing configuration/plugin/cache locations, treat them as cross-platform and security-sensitive:

- Use explicit, OS-appropriate path examples (especially Windows). Avoid ambiguous shorthand (like `~`) unless you’ve verified it expands correctly on Windows (e.g., to the user profile) and confirm behavior for supported profile types.
- For any generated/cached configuration written into the workspace (e.g., remote config), ensure repo hygiene:
  - Add `.gitignore` entries that match nested workspace folders.
  - Use recursive patterns (not just root-anchored ones) so the ignore works even when the workspace is inside a subfolder.
  - Document why the directories must be ignored (e.g., they may contain sensitive tokens/keys).

Example `.gitignore` snippet for workspace-written cached settings:
```text
**/.cline/enterprise/
**/.cline/remote-config/
```

Also sanity-check your ignore behavior (e.g., with `git check-ignore`) to confirm nested matches work as intended.