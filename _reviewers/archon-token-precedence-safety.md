---
title: Token Precedence Safety
description: When multiple authentication tokens are supported (e.g., generic GitHub
  tokens vs Copilot-specific tokens), enforce a deterministic, documented precedence
  and require explicit opt-in for fallback behavior.
repository: coleam00/Archon
label: Security
language: Yaml
comments_count: 1
repository_stars: 21089
---

When multiple authentication tokens are supported (e.g., generic GitHub tokens vs Copilot-specific tokens), enforce a deterministic, documented precedence and require explicit opt-in for fallback behavior.

Apply this to CI/workflows and any code that selects credentials:
- Prefer the Copilot-specific token whenever present (e.g., `COPILOT_GITHUB_TOKEN`).
- Only use generic `GH_TOKEN` / `GITHUB_TOKEN` if the caller explicitly opts in (e.g., `useLoggedInUser:false`).
- If both are provided, ensure the selection matches the precedence rule and is not left to “first one wins” ambiguity.

Example (workflow logic pattern):
```yaml
# Pseudocode: enforce precedence
env:
  COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}
  GH_TOKEN: ${{ secrets.GH_TOKEN }}

# Selection rule (conceptual):
# if COPILOT_GITHUB_TOKEN set -> use it
# else if GH_TOKEN/GITHUB_TOKEN set -> require explicit useLoggedInUser:false
# else -> fail
```

This prevents accidental use of the wrong credentials, reduces risk of unexpected permissions, and makes security-sensitive behavior consistent across environments.