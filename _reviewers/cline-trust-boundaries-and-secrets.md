---
title: Trust boundaries and secrets
description: 'Do not present easily-bypassed mechanisms as security controls, and
  never let untrusted or externally-controlled content influence security-sensitive
  behavior or gain access to secrets. Specifically:'
repository: cline/cline
label: Security
language: Other
comments_count: 3
repository_stars: 70886
---

Do not present easily-bypassed mechanisms as security controls, and never let untrusted or externally-controlled content influence security-sensitive behavior or gain access to secrets. Specifically:

1. **Be honest about guarantees.** If a mechanism (e.g., a hook script, a permission flag) can be trivially circumvented, don't document or design it as a security boundary. Frame it as a convenience/filtering feature instead (e.g., "keep the agent from wandering into build output") rather than implying it blocks malicious actors.

2. **Never trust attacker-controllable paths for policy or secrets.** When a workflow checks out untrusted content (e.g., a pull request branch), any config, hooks, or plugins from that checkout must not run with access to privileged credentials (tokens, API keys). Enforce policy from a trusted, non-checkout location (e.g., global hooks directory) instead of relying on repo-local files that an attacker-controlled PR could modify. Example: a CI job reviewing PRs should check out the base branch and fetch the diff via API, or delete `.cline`/`.clinerules` before running the privileged step, rather than trusting hooks/plugins from the PR's checkout.

3. **Protect cached secrets from accidental exposure.** If a tool writes credentials or sensitive cache files into the workspace, ensure they're excluded from version control with robust, recursive ignore patterns (e.g., `**/.cline/enterprise/` rather than `.cline/enterprise/`) so nested folders are also covered, and verify with `git check-ignore`.

Apply these checks whenever introducing automation, hooks, CI integrations, or caching that touches credentials or executes code from a source that isn't fully trusted.