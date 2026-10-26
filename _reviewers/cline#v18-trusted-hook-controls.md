---
title: Trusted Hook Controls
description: Treat hooks/plugins and any hook files shipped by a repository as untrusted.
  Enforce authorization with trusted/global configuration (not code that the model/PR
  can modify) and implement allow/deny decisions with strict input validation and
  exact allowlists.
repository: cline/cline#v18
label: Security
language: Other
comments_count: 3
repository_stars: 70884
---

Treat hooks/plugins and any hook files shipped by a repository as untrusted. Enforce authorization with trusted/global configuration (not code that the model/PR can modify) and implement allow/deny decisions with strict input validation and exact allowlists.

Apply:
1) Don’t use repo `.cline/hooks/` or `.clinerules/hooks/` as a security control—PRs can change them (and the checked-out hooks run with the job environment, including secrets).
2) Put blocking logic in a trusted location (e.g., a global `PreToolUse` hook in the runner/CI image) or remove/recreate the untrusted `.cline` directories before the step.
3) When auto-approving tool calls, validate the request payload shape and match whole commands (not prefixes/substring). Avoid “safe by string contains” logic.

Example (tool permission allowlist with input-shape validation):
```ts
const cline = await ClineCore.create({
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown; files?: unknown }

      if (request.toolName !== "run_commands") return { approved: false }
      if (!Array.isArray(input.commands)) return { approved: false }

      // Exact allowlist of command strings (no prefix/substring matching)
      const safe = new Set([
        "ls",
        "git status",
        "git log --oneline -20",
        "git diff --no-ext-diff --no-textconv", // example only; verify per your threat model
      ])

      const allAllowed = input.commands.every(
        (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
      )
      return { approved: allAllowed }
    }
  }
})
```

Example (trusted blocking via global `PreToolUse` hook):
- Place the hook in a trusted global directory (not the PR checkout), and cancel `run_commands` you don’t allow.
- If you must consume a repo, delete `/.cline` and `/.clinerules` (or checkout a base branch and extract diffs) before enabling autonomous tool execution.

Also: don’t market hook behavior as “security” unless the threat model guarantees the control can’t be bypassed; otherwise describe it as a best-effort guardrail (e.g., filtering out irrelevant/noisy inputs).