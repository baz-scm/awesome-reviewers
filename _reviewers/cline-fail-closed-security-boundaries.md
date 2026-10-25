---
title: Fail-Closed Security Boundaries
description: 'Adopt a single secure-by-default rule-set: **authentication/authorization
  gates must fail closed**, **secret-bearing data must never be logged**, and **sandbox/file
  boundaries must be enforced with real paths and deny escape hatches**.'
repository: ClInE/cLiNe
label: Security
language: TypeScript
comments_count: 13
repository_stars: 70838
---

Adopt a single secure-by-default rule-set: **authentication/authorization gates must fail closed**, **secret-bearing data must never be logged**, and **sandbox/file boundaries must be enforced with real paths and deny escape hatches**.

Apply this checklist:
1) **Auth/state mismatches must not proceed on implicit user dismissal**
- Treat only explicit user confirmation (e.g. button text) as authorization.
- Never accept a long-lived nonce as a CSRF/anti-forgery substitute; use per-request/short-lived state or a bounded set.

```ts
// Fail-closed auth callback example
if (authService.authNonce !== state) {
  const result = await vscode.window.showWarningMessage(
    `Could not verify auth state for ${uri.path}. Store token only if you started this sign-in.`,
    { modal: true },
    "Store",
  );
  if (result !== "Store") return; // undefined/dismiss => cancel
}
```

2) **Secrets must never appear in logs or error messages**
- In production, log only safe types (e.g., message + numbers/booleans); never serialize arbitrary args that might include tokens/URLs.
- Reduce any logged URL to `origin` (and ideally `origin + pathname` if you truly must keep path), stripping query/fragment/userinfo.

```ts
// Secret-safe URL log pattern
function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin;
  } catch {
    return "<invalid url>";
  }
}

logger.info(`Opening browser: ${redactUrlForLog(rawUrl)}`);
```

3) **Sandbox/file grants must be boundary-safe (fail closed)**
- Resolve real filesystem paths (e.g., `realpath`) and verify grants are inside the intended workspace.
- Deny read-write grants when the workspace root is a filesystem/volume root, home directory, or any ancestor outside your intended sandbox boundary.

```ts
// Boundary-safe grant example (conceptual)
const realCwd = await realpath(cwd);
if (isHomeOrAncestor(realCwd) || isVolumeRoot(realCwd)) {
  throw new Error("Refusing unsafe sandbox write root");
}
```

4) **Ownership/handshake takeovers must be explicit**
- Do not “best-effort” re-route work to the first attached registrant when a capability owner is gone.
- If the required owner disconnects/detaches, cancel/fail with a clear user message rather than changing behavior silently.

5) **Avoid bypassable assumptions in security limits**
- If output caps or policies are applied by names/identifiers, ensure they can’t be circumvented by custom names (prefer capability/tool identity over string matching when possible).

If you can’t prove (1) fail-closed behavior, (2) secret-safe observability, and (3) boundary enforcement from code + tests, treat the change as insecure-by-default and require a redesign.