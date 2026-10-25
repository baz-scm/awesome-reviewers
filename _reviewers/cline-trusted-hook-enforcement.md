---
title: Trusted Hook Enforcement
description: Use hooks and command allow-lists as *best-effort filtering*, not as
  a security boundary—unless the enforcement is done from a trusted location (workflow/global
  config), with strict input validation and conservative approvals.
repository: cline/CLINE
label: Security
language: Other
comments_count: 3
repository_stars: 70839
---

Use hooks and command allow-lists as *best-effort filtering*, not as a security boundary—unless the enforcement is done from a trusted location (workflow/global config), with strict input validation and conservative approvals.

Apply this standard:
1) Don’t rely on repository-controlled hooks for security
- Assume a PR/repo can modify `.cline/hooks/` or `.clinerules/hooks/`. If you must block tools, enforce via workflow-controlled/global hooks (e.g., a `PreToolUse` hook installed outside the checked-out PR) or delete/ignore repo `.cline*` dirs before running.

2) Validate tool inputs before making authorization decisions
- Treat model/tool inputs as untrusted. Check both type and shape before comparing/approving.

3) Be conservative with “safe commands”
- Avoid brittle heuristics (e.g., command-string prefix checks). Prefer exact allow-lists of specific commands *and only in trusted repositories/environments*. If the repo is untrusted, don’t assume flags make complex tools (like Git) safe.

Example (global hook-style deny with input-shape validation):
```ts
// In a trusted, global hook (not from the checked-out repo)
// Pseudocode: validate shape, then cancel disallowed calls.

function isRunCommandsRequest(input: any): input is { commands: string[] } {
  return input && Array.isArray(input.commands) && input.commands.every(c => typeof c === 'string');
}

export function onPreToolUse(event: any) {
  // Validate event shape before enforcement
  if (event?.hookName !== 'tool_call' && event?.hookName !== 'PreToolUse') return;

  const toolName = event?.tool_call?.name ?? event?.preToolUse?.toolName;
  const input = event?.tool_call?.input ?? event?.preToolUse?.parameters;

  if (toolName === 'run_commands' && isRunCommandsRequest(input)) {
    // Exact allow-list or block-list; don't rely on fragile prefix matching
    const allowed = new Set(['ls', 'cat']);
    const commands = input.commands.map(s => s.trim());
    const disallowed = commands.some(cmd => !allowed.has(cmd));
    if (disallowed) {
      return { stop: true, reason: 'run_commands blocked by trusted policy' };
    }
  }
}
```

When writing documentation or implementing policy, explicitly state the trust boundary: “enforced by workflow/global config, not by repo-provided hooks,” and ensure decisions are made only after strict input validation and conservative allow/deny logic.