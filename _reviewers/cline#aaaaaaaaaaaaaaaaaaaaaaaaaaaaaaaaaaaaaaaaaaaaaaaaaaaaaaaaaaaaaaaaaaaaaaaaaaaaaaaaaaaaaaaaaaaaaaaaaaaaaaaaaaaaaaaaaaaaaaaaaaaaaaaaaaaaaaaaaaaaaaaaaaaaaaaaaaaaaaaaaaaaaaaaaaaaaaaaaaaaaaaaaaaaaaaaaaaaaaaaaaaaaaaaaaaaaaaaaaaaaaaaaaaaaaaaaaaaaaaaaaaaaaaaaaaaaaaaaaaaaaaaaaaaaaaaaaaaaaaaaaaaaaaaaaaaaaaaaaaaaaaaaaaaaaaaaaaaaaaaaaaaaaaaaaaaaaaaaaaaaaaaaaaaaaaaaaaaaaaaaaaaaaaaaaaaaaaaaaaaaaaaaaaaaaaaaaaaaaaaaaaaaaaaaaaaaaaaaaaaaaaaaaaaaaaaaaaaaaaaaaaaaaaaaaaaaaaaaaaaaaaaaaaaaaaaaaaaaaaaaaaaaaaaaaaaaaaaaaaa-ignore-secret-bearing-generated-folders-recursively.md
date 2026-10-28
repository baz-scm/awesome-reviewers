---
title: Ignore secret-bearing generated folders recursively
description: When documenting or configuring version-control ignore rules for directories
  that tools generate and that may contain sensitive data (API keys, access tokens,
  cached credentials, etc.), always use recursive glob patterns rather than root-anchored
  ones, since the generating process may create the folder in any subdirectory a user
  happens to be working in,...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: Other
comments_count: 1
repository_stars: 70964
---

When documenting or configuring version-control ignore rules for directories that tools generate and that may contain sensitive data (API keys, access tokens, cached credentials, etc.), always use recursive glob patterns rather than root-anchored ones, since the generating process may create the folder in any subdirectory a user happens to be working in, not just the repository root. A root-anchored pattern such as `.cline/enterprise/` will fail to match the same folder nested under a subdirectory, leaving secrets unprotected and liable to be committed.

Use patterns like `**/.cline/enterprise/` and `**/.cline/remote-config/` instead, and verify coverage with `git check-ignore <path>` against both root-level and nested test paths before merging. Additionally, document in-line why the ignore rule exists (e.g., "this folder may contain prompt storage access keys") so future maintainers understand the security rationale and don't inadvertently narrow or remove the pattern.

Example:
```text
# Wrong: only matches at repo root
.cline/enterprise/
.cline/remote-config/

# Correct: matches at any depth
**/.cline/enterprise/
**/.cline/remote-config/
```</description>
</invoke>
