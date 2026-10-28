---
title: Isolate untrusted repo content
description: Never let content checked out from an external or untrusted source (a
  pull request branch, a nested subfolder, a cached config file) silently gain access
  to secrets or elevated privileges in automated jobs.
repository: "cline/cline\r\n"
label: Security
language: Other
comments_count: 2
repository_stars: 70946
---

Never let content checked out from an external or untrusted source (a pull request branch, a nested subfolder, a cached config file) silently gain access to secrets or elevated privileges in automated jobs.

When a CI job checks out a pull request and runs an agent with auto-approve/elevated permissions, any hooks, plugins, or config files present in that checkout (e.g. `.cline/hooks/`, `.clinerules/hooks/`) can be merged into the job's execution context and run with the full job environment, including tokens like `GH_TOKEN`. A malicious PR could use this to exfiltrate secrets or run arbitrary commands. Mitigate this by not checking out the PR head directly for review steps — instead check out the base branch and fetch the diff via `gh pr diff` — or explicitly delete repo-controlled hook/plugin directories (`.cline/`, `.clinerules/`) before the review step runs. Only use a global, non-repo-controlled `PreToolUse` hook as a secondary safeguard, since repo-local hooks can be modified by the very PR being reviewed.

Similarly, any files your tooling writes into the workspace that may contain sensitive material (cached settings, access keys, tokens) must be reliably excluded from version control regardless of where in the repo tree they land. Use recursive ignore patterns instead of root-anchored ones, since a user may open or commit from a subfolder:

```text
# Wrong: only matches at repo root
.cline/enterprise/
.cline/remote-config/

# Right: matches at any depth
**/.cline/enterprise/
**/.cline/remote-config/
```

Verify ignore rules with `git check-ignore` on a nested path before relying on them. Treat any directory that can hold credentials or tokens as a security boundary: assume it can be committed or exposed unless you've proven otherwise.</description>
</invoke>
