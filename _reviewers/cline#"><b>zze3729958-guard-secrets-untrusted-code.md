---
title: Guard secrets untrusted code
description: Treat any code or configuration from an untrusted source (a checked-out
  pull request, a model-writable script, etc.) as hostile, and never let it execute
  with access to secrets or credentials. Enforce trust boundaries using the platform's
  real permission system instead of application-level checks that the same untrusted
  source can disable.
repository: cline/cline#"><b>zze3729958
label: Security
language: Other
comments_count: 3
repository_stars: 71067
---

Treat any code or configuration from an untrusted source (a checked-out pull request, a model-writable script, etc.) as hostile, and never let it execute with access to secrets or credentials. Enforce trust boundaries using the platform's real permission system instead of application-level checks that the same untrusted source can disable.

Concretely:
- Scope secrets using platform permissions (e.g., a CI job's `permissions` block limiting `GH_TOKEN`), not a hook or script that lives inside the untrusted checkout — a PR can modify its own `.cline/hooks` and defeat a hook meant to restrain it.
- When processing untrusted input in automation (e.g., reviewing a PR), avoid running any step with secret access against the untrusted checkout: check out the base branch and pull the diff separately (e.g. `gh pr diff`), or delete `.cline`/`.clinerules` before the step runs. Only trust hooks/plugins from global, non-checked-out locations as an extra enforcement layer.
- Don't present a fragile, easily bypassed script-based control as a security mechanism. If the same actor it's meant to constrain can disable it, reframe it honestly (e.g., "filters out irrelevant files") rather than implying a security guarantee.
- Exclude any files that may cache secrets (tokens, keys, settings) from version control using robust, recursive `.gitignore` patterns rather than root-anchored ones, since the working directory may be a subfolder:
```text
**/.cline/enterprise/
**/.cline/remote-config/
```
Verify with `git check-ignore` against a nested path, and note in comments why the folder is sensitive (e.g., it contains access keys).

Always identify the real trust boundary first, enforce it with the platform's permission/credential system, and make sure any additional script-based checks are robust against the specific actor they aim to restrict — or are not described as security at all.