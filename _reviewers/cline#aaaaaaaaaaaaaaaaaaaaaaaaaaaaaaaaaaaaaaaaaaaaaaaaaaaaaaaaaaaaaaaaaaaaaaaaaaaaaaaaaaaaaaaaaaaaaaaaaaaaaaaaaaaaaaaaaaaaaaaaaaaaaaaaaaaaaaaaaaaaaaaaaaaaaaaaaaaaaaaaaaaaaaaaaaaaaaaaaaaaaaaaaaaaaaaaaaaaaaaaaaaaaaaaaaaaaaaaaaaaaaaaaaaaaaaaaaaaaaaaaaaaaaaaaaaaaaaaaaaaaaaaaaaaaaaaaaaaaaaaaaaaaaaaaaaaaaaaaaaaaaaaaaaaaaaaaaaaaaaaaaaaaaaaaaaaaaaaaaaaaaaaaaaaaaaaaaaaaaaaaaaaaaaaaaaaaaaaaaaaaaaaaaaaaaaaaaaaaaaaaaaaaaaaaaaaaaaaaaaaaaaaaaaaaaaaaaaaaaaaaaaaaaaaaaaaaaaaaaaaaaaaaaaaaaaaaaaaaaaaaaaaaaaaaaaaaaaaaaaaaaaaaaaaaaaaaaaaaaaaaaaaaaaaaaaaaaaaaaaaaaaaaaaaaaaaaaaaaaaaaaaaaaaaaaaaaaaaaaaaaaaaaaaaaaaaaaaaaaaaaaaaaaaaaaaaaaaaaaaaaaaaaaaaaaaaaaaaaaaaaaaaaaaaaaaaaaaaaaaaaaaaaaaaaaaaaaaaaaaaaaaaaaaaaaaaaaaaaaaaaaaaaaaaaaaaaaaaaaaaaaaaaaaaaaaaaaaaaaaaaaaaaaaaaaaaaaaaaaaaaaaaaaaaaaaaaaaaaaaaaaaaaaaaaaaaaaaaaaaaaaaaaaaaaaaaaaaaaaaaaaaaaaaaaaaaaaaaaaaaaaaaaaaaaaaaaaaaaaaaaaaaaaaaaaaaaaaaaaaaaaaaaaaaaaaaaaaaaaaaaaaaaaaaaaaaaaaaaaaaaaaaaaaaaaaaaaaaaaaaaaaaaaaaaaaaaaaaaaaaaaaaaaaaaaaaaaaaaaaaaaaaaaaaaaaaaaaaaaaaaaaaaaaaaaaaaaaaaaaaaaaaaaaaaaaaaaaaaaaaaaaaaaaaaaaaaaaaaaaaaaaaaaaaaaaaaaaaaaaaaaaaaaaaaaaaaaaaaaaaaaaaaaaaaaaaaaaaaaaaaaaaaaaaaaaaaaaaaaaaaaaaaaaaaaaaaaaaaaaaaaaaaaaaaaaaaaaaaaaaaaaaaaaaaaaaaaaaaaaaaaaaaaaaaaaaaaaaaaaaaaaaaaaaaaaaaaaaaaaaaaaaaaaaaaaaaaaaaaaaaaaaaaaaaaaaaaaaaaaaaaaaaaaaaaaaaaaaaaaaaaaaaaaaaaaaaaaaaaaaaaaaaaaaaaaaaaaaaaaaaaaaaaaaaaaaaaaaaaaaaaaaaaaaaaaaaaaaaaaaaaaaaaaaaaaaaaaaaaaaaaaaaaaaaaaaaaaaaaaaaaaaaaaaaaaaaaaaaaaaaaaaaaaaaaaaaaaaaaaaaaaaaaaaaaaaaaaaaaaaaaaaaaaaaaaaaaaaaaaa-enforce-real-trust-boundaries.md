---
title: Enforce real trust boundaries
description: 'When designing anything that gates risky actions (shell commands, tool
  calls, hooks), identify the actual trust boundary and enforce controls there, not
  at a layer an attacker or untrusted input can bypass. Command allowlists based on
  string/prefix matching (e.g. approving `git diff` or `git status`) are not safe:
  tool-specific config like `diff.external`...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: Other
comments_count: 4
repository_stars: 70965
---

When designing anything that gates risky actions (shell commands, tool calls, hooks), identify the actual trust boundary and enforce controls there, not at a layer an attacker or untrusted input can bypass. Command allowlists based on string/prefix matching (e.g. approving `git diff` or `git status`) are not safe: tool-specific config like `diff.external` or `core.fsmonitor` can make an "allowed" command execute an arbitrary external program, so no flag or prefix check makes a command provably safe in an untrusted repository. Don't market such filters as security mechanisms if the model (or an attacker) can trivially defeat them—either close the bypasses or document the mechanism as a convenience/filtering feature, not a security guarantee. Similarly, never let logic from an untrusted, checked-out source (e.g. a pull request branch) control privileged execution: if a CI job checks out a PR, hooks or config files in that checkout can be modified by the PR itself and will still run with the job's credentials (e.g. `GH_TOKEN`). The real boundary in that case is the credential/permission scope of the job, or an execution step that excludes/ignores untrusted repo content (checkout the base branch, strip `.cline`/`.clinerules` before running, or rely on hooks placed outside the untrusted checkout). Finally, when sensitive material (API keys, cached credentials) is written to disk for caching/config purposes, ensure it can never be committed: use recursive ignore patterns (`**/.cline/enterprise/`, not just `.cline/enterprise/`) so nested copies in subfolders are also excluded, and verify with `git check-ignore` that the pattern actually matches nested paths.

Example of a flawed "safe list" vs. a documented limitation:
```js
// NOT safe: `git diff` can trigger diff.external or core.fsmonitor, running arbitrary programs
const safeCommands = new Set(["ls", "git status", "git diff", "git log --oneline -20"])

// Safer: narrow the list and document the real boundary
// Only approve Git commands automatically in repositories you trust.
const safeCommands = new Set(["ls", "git status", "git log --oneline -20"])
```

When documenting or implementing any gate, ask: "Can the untrusted side (model output, PR contents, repo config) change the actual behavior of this check?" If yes, treat it as a convenience feature and enforce the real security guarantee at the credential, permission, or execution-isolation layer instead.