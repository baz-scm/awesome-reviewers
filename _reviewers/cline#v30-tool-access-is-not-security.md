---
title: Tool Access Is Not Security
description: Do not treat “ignore” files or repository-provided hooks as a security/access-control
  boundary. If your system can execute or read files/tools via the model, assume the
  model/inputs can bypass best-effort filtering.
repository: cline/cline#v30
label: Security
language: Other
comments_count: 4
repository_stars: 70894
---

Do not treat “ignore” files or repository-provided hooks as a security/access-control boundary. If your system can execute or read files/tools via the model, assume the model/inputs can bypass best-effort filtering.

Apply this standard:
- **Trust boundaries:** Only enforce access control with policies you control (e.g., global hooks/config). **Do not rely on hooks/plugins shipped in a repo/PR checkout**, because the PR can modify them.
- **Allowlists over assumptions:** When approving tool calls, use **strict allowlists** and **validate input shape** before approving. Do not rely on “safe flags” for complex tools—real-world configs/escape hatches (e.g., Git helpers/config) can make “read-only” commands unsafe in untrusted repos.
- **Be explicit about intent:** If you can’t guarantee non-bypassable enforcement, **frame hooks/filters as “filtering irrelevant content,” not “blocking access”**.

Example (policy-style allow/deny around tool execution):
```ts
// Example: approve only a tiny set of truly safe commands
const cline = await ClineCore.create({
  clientName: "secure-policy",
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown }

      // Enforce shape first
      if (request.toolName !== "run_commands" || !Array.isArray(input.commands)) {
        return { approved: false }
      }

      // Approve only exact, minimal commands (repo must be trusted)
      const safe = new Set(["ls", "git status"])
      const commands = input.commands.filter((x): x is string => typeof x === "string")

      // If repo trust is unknown/untrusted, refuse to run commands.
      if (!process.env.REPO_TRUSTED) return { approved: false }

      if (commands.length === input.commands.length && commands.every(c => safe.has(c.trim()))) {
        return { approved: true }
      }

      return { approved: false }
    }
  }
})
```

For CI/PR workflows, prefer a **global `PreToolUse` hook** (or delete/disable repo-provided `.cline/` rules before the step) so untrusted contributions can’t change the enforcement.
