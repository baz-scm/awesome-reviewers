---
title: Enforce Trust-Boundary Controls
description: Security-sensitive behavior must be enforced from trusted inputs and
  with validated permission logic; do not rely on mechanisms that an untrusted repository
  can change or that are known to be ineffective as access control.
repository: ClInE/cLiNe
label: Security
language: Other
comments_count: 5
repository_stars: 70838
---

Security-sensitive behavior must be enforced from trusted inputs and with validated permission logic; do not rely on mechanisms that an untrusted repository can change or that are known to be ineffective as access control.

Apply these rules:

1) Don’t treat “ignore/filter” files as security boundaries
- If the tool/runtime can still access files via explicit requests, assume filters are not protective.
- Prefer hard enforcement that can cancel/block execution (e.g., task/tool blocking via hooks), and document that filters are only meant to reduce irrelevant data.

2) Don’t rely on repo-provided hooks for enforcement
- If you check out a PR/repo, that code can modify hooks/plugins/config used during execution.
- Enforce deny/cancel behavior via global (user/host) hook locations or organization-controlled remote configuration.

3) Validate tool permission inputs by shape
- Permission checks should parse/validate the tool request structure (types/fields) before deciding.
- Avoid brittle string prefix checks that can be bypassed by different argument formatting.

4) Use minimal, trust-aware allowlists for commands
- Do not assume “read-only” commands are harmless in untrusted repositories (e.g., Git may execute hooks/programs depending on config).
- Only allow an explicitly vetted set of commands/flags, and only in repositories you trust.

5) Prevent committing sensitive cached configuration
- Add cached settings directories to .gitignore using recursive patterns so nested folders are covered.

Example patterns:

- Trust-boundary hook enforcement (global path, not repo):
```sh
# ~/.cline/hooks/PreToolUse (example logic)
# Cancel run_commands unless it matches your allowlist.
# Read hook JSON from stdin, inspect tool_call.name + input shape, and exit/emit a cancel signal.
```

- Shape-validated command approval:
```ts
type RunCommandsInput = { commands?: unknown };

function approve(request: {
  toolName: string;
  input: unknown;
}): { approved: boolean } {
  const input = request.input as RunCommandsInput;
  const allow = new Set(["ls", "git status"]);

  if (request.toolName !== "run_commands") return { approved: false };
  if (!Array.isArray(input.commands)) return { approved: false };

  const ok = input.commands.every(
    (c) => typeof c === "string" && allow.has(c.trim())
  );
  return { approved: ok };
}
```

- Secret hygiene:
```gitignore
**/.cline/enterprise/
**/.cline/remote-config/
```