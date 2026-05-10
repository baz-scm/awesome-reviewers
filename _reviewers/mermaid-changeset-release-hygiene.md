---
title: Changeset release hygiene
description: 'Ensure changeset PRs produce correct and minimal release automation
  output.


  Apply these rules before submitting:

  - **Create changesets only for user/release-relevant changes.** If it’s documentation-only,
  **do not** add a changeset.'
repository: mermaid-js/mermaid
label: CI/CD
language: Markdown
comments_count: 8
repository_stars: 87952
---

Ensure changeset PRs produce correct and minimal release automation output.

Apply these rules before submitting:
- **Create changesets only for user/release-relevant changes.** If it’s documentation-only, **do not** add a changeset.
- **Scope packages precisely.** A changeset header should include **only the packages that are actually affected**.
- **Split multi-package changes when entries should land in separate release notes.** If one change affects two packages independently, use **separate changeset files** rather than combining messages in one.
- **Choose the semver level based on user impact:**
  - **`major`**: reserved for **breaking changes**.
  - **`patch`**: bug fixes / no user-facing behavior change.
  - **`minor`**: non-breaking new functionality/improvements that affect users.
  - Avoid using non-standard bump labels (e.g., `chore`) when `major/minor/patch` is expected.

Example (correct semver selection + scoped header):
```md
---
'mermaid': patch
---
fix: Correct diagram rendering regression
```

Example (split multi-package change into separate files):
- File A: bump only `@mermaid-js/examples`
- File B: bump only `mermaid`
with each file containing only its relevant release-note text and semver decision.