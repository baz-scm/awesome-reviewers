---
title: Accurate security controls
description: Only describe a mechanism as a security control if it actually enforces
  the boundary it claims; if it can be trivially bypassed (e.g., a user-editable script
  that filters tool calls), document it as a convenience or filtering feature instead,
  not as protection against a motivated actor. Separately, when a feature writes files
  to a workspace that may contain...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Security
language: Other
comments_count: 2
repository_stars: 71067
---

Only describe a mechanism as a security control if it actually enforces the boundary it claims; if it can be trivially bypassed (e.g., a user-editable script that filters tool calls), document it as a convenience or filtering feature instead, not as protection against a motivated actor. Separately, when a feature writes files to a workspace that may contain secrets (API keys, access tokens, cached credentials), ensure those paths are excluded from version control with patterns that match the file regardless of where in the directory tree it ends up. Prefer recursive glob patterns (e.g. `**/.cline/enterprise/`) over root-anchored ones (`.cline/enterprise/`), since the latter won't match the folder if a user opens or commits from a subdirectory. Verify exclusion rules with `git check-ignore <path>` against both root-level and nested locations before shipping. Example:

```text
# Wrong: only matches if repo root is the git root
.cline/enterprise/

# Right: matches at any depth
**/.cline/enterprise/
```</description>
</invoke>
