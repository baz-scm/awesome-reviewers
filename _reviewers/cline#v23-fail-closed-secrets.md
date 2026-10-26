---
title: Fail Closed Secrets
description: Security-sensitive code must be explicit about trust boundaries and must
  fail closed by default—especially on (1) authentication/callback flows, (2) log/output
  of potentially credential-bearing data, and (3) filesystem/sandbox write scopes.
repository: cline/cline#v23
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70889
---

Security-sensitive code must be explicit about trust boundaries and must fail closed by default—especially on (1) authentication/callback flows, (2) log/output of potentially credential-bearing data, and (3) filesystem/sandbox write scopes.

Apply this standard:

1) Auth/callback anti-forgery must not continue on ambiguous UI outcomes
- Do not “prompt then proceed” unless the user action is an explicit allow-list value; treat dismiss/ESC/undefined as “deny”.
- Keep state nonces effective (short-lived/rotating) and never treat mismatches as optional CSRF protection.

Example pattern:
```ts
if (authService.authNonce !== state) {
  const result = await vscode.window.showWarningMessage(
    `Auth could not be verified. Store token from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (result !== "Store") return;
}
// Only proceed to store token after verified state (or an explicit allow-list override).
```

2) Logs must not include credentials, OAuth codes, or userinfo
- Redact URLs before logging (origin/host only) and never concatenate expanded secrets into error strings.
- In production, Logger formatting must be restrictive: only allow safe primitives; treat error serialization as untrusted.

Example redaction helper:
```ts
export function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url);
    return parsed.origin === "null" ? `${parsed.protocol}<redacted>` : parsed.origin;
  } catch {
    return "<invalid url>";
  }
}

// Usage
Logger.info(`Opening browser: ${redactUrlForLog(browserUrl)}`);
```

3) Sandbox/write scopes must be validated and bounded
- When granting write access (e.g., “only allow edits in project directory”), validate that the real resolved write root is a legitimate subdirectory, not a filesystem root, not a home/ancestor, and not an overly broad parent.
- Prefer `realpath`/canonicalization and deny “dangerous ancestors” with a clear error.

Example policy check sketch:
```ts
const realCwd = await fs.realpath(cwd);
const home = await fs.realpath(os.homedir());
const root = path.parse(realCwd).root; // filesystem root
if (realCwd === root || realCwd === home || realCwd.startsWith(home + path.sep) ) {
  throw new Error("Refusing unsafe sandbox write root");
}
```

4) Path/input boundary checks must be robust
- Enforce workspace containment rules using canonical paths, not just string checks.
- When allowing symlinks, document the intent and still ensure the resolved target cannot escape the security boundary.
- Treat “sensitive file blocking” as defense-in-depth: filename-only checks are brittle; prefer path pattern + canonical path checks wherever feasible.

Checklist for PRs in security-sensitive areas:
- “Fail closed” verified for mismatches/dismissals/ownership disconnects.
- All logs of URLs/errors are redacted/sanitized; production logging is restrictive.
- Any filesystem write scope is canonicalized and checked against dangerous roots/ancestors.
- Any path boundary logic is tested for traversal edge cases and (if allowed) symlink behavior.