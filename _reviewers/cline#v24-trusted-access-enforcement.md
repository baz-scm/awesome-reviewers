---
title: Trusted Access Enforcement
description: Treat any “ignore/filter” mechanism as documentation only, not a security
  boundary. Enforce access control at trusted enforcement points, validate inputs
  before making security decisions, and assume repository-controlled content/config
  is untrusted.
repository: cline/cline#v24
label: Security
language: Other
comments_count: 4
repository_stars: 70891
---

Treat any “ignore/filter” mechanism as documentation only, not a security boundary. Enforce access control at trusted enforcement points, validate inputs before making security decisions, and assume repository-controlled content/config is untrusted.

Apply these rules:
- **Enforcement > filters:** If a mechanism only changes what the model auto-loads, it does not prevent explicit reads or command execution. Require an enforcement hook (or equivalent) that blocks disallowed tool calls.
- **Strict allowlists with input validation:** Before approving a tool call, validate the tool input shape and match **exact** allowed commands (no prefix/substring checks). Don’t “whitelist” commands based on assumed safe flags in untrusted repos.
- **Don’t trust repo-provided hooks/config:** If a PR/workspace checkout can modify hook files or plugins, those controls are bypassable. Prefer global/trusted hooks, or change the workflow so repo-controlled `.cline*` content is not used.
- **Protect workspace-written security artifacts:** If your system writes cached org settings/rules into the workspace (often containing secrets like access keys), ensure they are covered by `.gitignore` using recursive patterns.

Example (command allowlisting via validated input):
```ts
async function requestToolApproval(request: any) {
  // Validate tool input shape first
  const input = request.input as { commands?: unknown; files?: unknown }

  if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
    const safe = new Set(["ls", "git status", "git log --oneline -20"])

    // Approve only exact, trimmed commands
    const ok = input.commands.every(
      (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
    )

    if (ok) return { approved: true }
  }

  return { approved: false }
}
```

Example (don’t commit generated remote/security config):
```gitignore
**/.cline/enterprise/
**/.cline/remote-config/
```