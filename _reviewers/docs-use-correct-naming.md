---
title: Use Correct Naming
description: Use naming conventions that clearly distinguish placeholders from required
  identifiers, follow platform identifier constraints, and keep variable scope/semantics
  correct.
repository: github/docs
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 21111
---

Use naming conventions that clearly distinguish placeholders from required identifiers, follow platform identifier constraints, and keep variable scope/semantics correct.

- **Placeholders:** If a value is a placeholder, use your docs’ standard placeholder format consistently (e.g., hyphenated: `YOUR-CONNECTION-ID`).
- **Required identifiers:** If the name is a real environment variable or action input key, keep it **exactly** as required by the platform/action (do not “normalize” underscores/hyphens).
- **Identifier character rules:** Don’t broaden allowed characters in identifiers. If the platform disallows spaces (or you’re defining rules for something that disallows spaces), **do not** permit spaces in examples/specs.
- **Scope safety:** Don’t mix GitHub/platform-specific variable documentation with OS/system user-home variables (avoid encouraging edits to or reliance on shell `HOME`). Prefer documenting the platform-provided paths (for example, `GITHUB_WORKSPACE`).
- **Semantic accuracy:** Ensure variable names’ descriptions match runtime behavior (don’t swap “model id” vs “wire model/deployment name”).

Example (placeholder vs required env var):
```yaml
- name: Sign in with OIDC
  uses: docker/login-action@<pinned-sha>
  with:
    username: YOUR-DOCKER-ORG          # placeholder formatting
  env:
    DOCKERHUB_OIDC_CONNECTIONID: YOUR-CONNECTION-ID  # required env var name kept exact
```
