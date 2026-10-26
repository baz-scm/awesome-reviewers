---
title: Secure Tool Access
description: 'Treat any model/tool interaction as untrusted: repo-provided files/configs
  and “filtering” mechanisms are not security boundaries.


  **Standard**

  - **Don’t rely on bypassable filters** (e.g., ignore lists that only affect what’s
  *loaded*). If you need enforcement, implement it in an **effective interception
  point** (e.g., a trusted `PreToolUse` hook) and...'
repository: cline/cline#v28
label: Security
language: Other
comments_count: 4
repository_stars: 70893
---

Treat any model/tool interaction as untrusted: repo-provided files/configs and “filtering” mechanisms are not security boundaries.

**Standard**
- **Don’t rely on bypassable filters** (e.g., ignore lists that only affect what’s *loaded*). If you need enforcement, implement it in an **effective interception point** (e.g., a trusted `PreToolUse` hook) and don’t describe it as security if it can be defeated.
- **Don’t trust repository-controlled policy** for security. If a PR/checkout can modify `.cline/hooks/` or plugins, that policy must be treated as attacker-controlled. Prefer **workflow/global hooks** (outside the repo) or other job-level controls.
- **Use least-privilege with input validation**: validate the tool request structure before applying allow/deny logic. Only approve a narrow, explicitly-defined set of actions.
- **Be cautious with “safe command” lists**: complex tools like Git are not reliably safe in untrusted repositories (hooks/subcommands/config can execute code). Either remove such commands from approvals or only allow them in contexts you fully trust.

**Example: trusted PreToolUse hook (deny by default)**
```js
// ~/.cline/hooks/PreToolUse (conceptual)
// Receives JSON describing the event.
const event = JSON.parse(require('fs').readFileSync(0, 'utf8'));

// CLI/desktop: event.hookName identifies type; run_commands example
// Validate input shape before using it.
const input = event?.preToolUse?.parameters ?? event?.tool_call?.input;
const commands = Array.isArray(input?.commands) ? input.commands : null;

const allowed = new Set(['ls']); // keep it narrow

if (event.tool_call?.name === 'run_commands') {
  const ok = commands && commands.every(c => typeof c === 'string' && allowed.has(c.trim()));
  if (!ok) {
    // cancel/deny the tool call (exact mechanism depends on your hook runtime)
    process.stdout.write(JSON.stringify({ approved: false, cancel: true }));
    process.exit(1);
  }
}
```

**Checklist**
- Enforcement point is **trusted** (not repo-editable).
- Policy is **effective** (can’t be bypassed by explicit reads/mentions).
- Requests are **validated by shape**.
- Allowlists are **narrow**; complex commands are avoided or only used in trusted repos.
- Secrets/config artifacts (e.g., remote config caches) are **not committed** to source control.