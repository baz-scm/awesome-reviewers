---
title: Safe spawn and permission validation
description: 'Enforce security for any code that turns user/config inputs into subprocess
  execution or permission settings.


  Apply these rules:

  1) Spawn safely

  - Use `spawn(binary, args, ...)` with an args array.'
repository: coleam00/Archon
label: Security
language: TypeScript
comments_count: 5
repository_stars: 21089
---

Enforce security for any code that turns user/config inputs into subprocess execution or permission settings.

Apply these rules:
1) Spawn safely
- Use `spawn(binary, args, ...)` with an args array.
- Never build a shell command via string concatenation.

2) Validate inputs that affect execution
- For paths to executables or binaries (from env/config/vendor/autodetect), require they are executable by the current user (don’t just check `existsSync`).
- For “name”-type inputs that will be joined into paths, enforce a strict contract (reject absolute paths, path separators, `.`/`..`, basename mismatches; trim whitespace; report invalid entries instead of silently accepting).

3) Make permission precedence unambiguous
- When allow/deny lists overlap, ensure deny takes precedence (e.g., remove deny-listed tools from the allow set before emitting flags).

4) Don’t rely on pre-parsing
- Emit security warnings/guardrails based on the final computed argv so `extraArgs` can’t bypass safety checks.

Example (deny-wins + safe argv building):
```ts
function buildArgs({ prompt, config, nodeConfig, extraArgs }: any): string[] {
  const args: string[] = ['-p', prompt];

  const allow = new Set([...(config.allowTools ?? []), ...(nodeConfig?.allowed_tools ?? [])]);
  const deny = new Set([...(config.denyTools ?? []), ...(nodeConfig?.denied_tools ?? [])]);
  for (const t of deny) allow.delete(t); // deny wins

  for (const t of allow) args.push(`--allow-tool=${t}`);
  for (const t of deny) args.push(`--deny-tool=${t}`);

  // extraArgs appended only after all security decisions are derived from final argv
  args.push(...(extraArgs ?? []));
  return args;
}

// Later: scan final argv for broad flags and warn; then spawn(binary, args, ...).
```

This reduces risks of command injection, path traversal/file misuse, and silent permission escalation.