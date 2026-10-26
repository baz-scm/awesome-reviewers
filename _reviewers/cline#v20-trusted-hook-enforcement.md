---
title: Trusted Hook Enforcement
description: 'Do not rely on hooks/plugins from untrusted sources (e.g., repository
  `.cline/hooks/` / `.clinerules/hooks/` after checkout) to provide security or protect
  secrets. Treat hooks as best-effort convenience (e.g., filtering), and implement
  real authorization by:'
repository: cline/cline#v20
label: Security
language: Other
comments_count: 3
repository_stars: 70886
---

Do not rely on hooks/plugins from untrusted sources (e.g., repository `.cline/hooks/` / `.clinerules/hooks/` after checkout) to provide security or protect secrets. Treat hooks as best-effort convenience (e.g., filtering), and implement real authorization by:
- Enforcing policy in *trusted* locations (global hooks or CI job configuration applied outside the PR).
- Using strict allowlists/denylists with input-shape validation (never assume the tool input is well-formed).
- Avoiding unsafe assumptions about “read-only” commands when tool behavior depends on repository configuration.

Practical pattern (block disallowed tool execution with a trusted `PreToolUse` hook):
```js
// ~/.cline/hooks/PreToolUse.js (trusted/global)
// Read JSON event from stdin, inspect tool call, and cancel disallowed ones.
import fs from 'node:fs';

const event = JSON.parse(fs.readFileSync(0, 'utf8'));

// CLI event: hookName=tool_call, tool_call.name is the tool name.
if (event?.hookName === 'tool_call' && event?.tool_call?.name === 'run_commands') {
  const input = event.tool_call.input;

  // Example: if the input includes commands[], allow only a tiny set.
  const commands = Array.isArray(input?.commands) ? input.commands : null;
  const allowed = new Set(['ls', 'git status']);

  const allAllowed =
    Array.isArray(commands) && commands.every((c) => typeof c === 'string' && allowed.has(c.trim()));

  if (!allAllowed) {
    // Cancel the task/tool call (shape depends on the hook API).
    // Use the documented cancel/stop mechanism for your hook runtime.
    process.stdout.write(JSON.stringify({ cancel: true }));
    process.exit(0);
  }
}
```

Documentation rule of thumb: if you mention hooks as a mitigation, frame them as *filtering/guardrails*, not a security boundary—because a determined actor can often bypass or modify hook content when it’s sourced from untrusted code.