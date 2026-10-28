---
title: Enforce real trust boundaries
description: 'When documenting or implementing any mechanism that restricts, approves,
  or isolates agent/automation behavior, verify it actually holds against adversarial
  or untrusted input before presenting it as a security control. Concretely:'
repository: cline/cline#$(sleep 4)
label: Security
language: Other
comments_count: 4
repository_stars: 70978
---

When documenting or implementing any mechanism that restricts, approves, or isolates agent/automation behavior, verify it actually holds against adversarial or untrusted input before presenting it as a security control. Concretely:

- Don't label a mechanism as "security" if it can be trivially bypassed by the thing it's meant to constrain. A hook that just filters irrelevant files (e.g., minified build output) should be documented as a convenience filter, not a safeguard against a misbehaving model.
- Build allowlists/denylists against exact, fully-specified operations, not brittle string prefixes. `git diff` looks safe but can execute arbitrary programs via `diff.external` or `core.fsmonitor`; matching whole, explicit commands (e.g., `git diff --no-ext-diff --no-textconv`) and documenting the residual trust assumption ("only auto-approve in repos you trust") is required.
- Never rely on enforcement logic that lives inside content the attacker controls. In CI, a pull request checkout can include its own `.cline/hooks/`, `.clinerules/hooks/`, or `.cline/plugins/`, which will run with the job's full environment and secrets (e.g., `GH_TOKEN`). Enforce restrictions from a location outside the untrusted checkout (a global hook in `~/.cline/hooks/`), or avoid executing the untrusted content altogether (check out the base branch and diff separately, or delete `.cline`/`.clinerules` before running).
- Treat any file or cache that may contain secrets (API keys, tokens, prompt-storage credentials) as sensitive by default. Exclude it from version control with recursive glob patterns (e.g., `**/.cline/enterprise/`, `**/.cline/remote-config/`) rather than root-anchored ones, since the sensitive folder can appear in any subdirectory.

Example of a correct, narrowly-scoped auto-approval check:

```ts
// Approve a fixed set of read-only commands only in trusted repos.
const safeCommands = new Set(["ls", "git status", "git log --oneline -20"])
if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
    return { approved: true }
  }
}
```

Before adding any new permission, hook, or ignore rule, ask: "What happens if the input/content this is supposed to block is actively adversarial?" If the control fails that test, redesign it or stop calling it a security boundary.</description>
</invoke>
