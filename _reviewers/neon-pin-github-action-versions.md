---
title: Pin GitHub action versions
description: Always pin GitHub Actions to specific commit hashes instead of using
  major/minor version tags (like @v4). This ensures reproducible builds and prevents
  supply chain attacks through compromised action versions.
repository: neondatabase/neon
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 19015
---

Always pin GitHub Actions to specific commit hashes instead of using major/minor version tags (like @v4). This ensures reproducible builds and prevents supply chain attacks through compromised action versions.

Example:
```yaml
# Don't do this:
- uses: actions/checkout@v4
- uses: actions/cache@v4

# Do this instead:
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
- uses: actions/cache@5a3ec84eff668545956fd18022155c47e93e2684 # v4.2.3
```

Include the version number in a comment after the commit hash for better readability and version tracking. This practice should be applied consistently across all workflow files. Consider implementing a linter to enforce this standard automatically.