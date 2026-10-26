---
title: Fail-closed Security Boundaries
description: 'Security-sensitive flows must default to the safest outcome: never “paper
  over” mismatches, never over-grant write access, and never leak credentials in logs.'
repository: cline/cline#v11
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70871
---

Security-sensitive flows must default to the safest outcome: never “paper over” mismatches, never over-grant write access, and never leak credentials in logs.

Apply these rules:
1) Auth/callback/state checks must fail closed
- If a security check (e.g., OAuth callback `state`, capability ownership, session ownership) doesn’t verify, do not store tokens or continue. Only proceed on an explicit allow action.

Example (fail closed on state mismatch):
```ts
if (authNonce !== state) {
  const res = await vscode.window.showWarningMessage(
    `Authentication could not be verified. Continue?`,
    { modal: true },
    "Store",
  );
  if (res !== "Store") return; // dismissed => block
}
// safe: only now persist/store token
```

2) Least-privilege: validate sandbox write roots
- When granting filesystem write access (sandbox/MXC), ensure granted paths are constrained to the intended project directory (and reject real-paths that are/contain volume roots, home, or unsafe ancestors). Resolve symlinks/real paths and fail closed with a clear user message if the computed boundary is unsafe.

3) Secret-safe logging/telemetry
- In production, never log raw errors/strings that may contain OAuth codes, tokens, credentials in URLs, or sensitive file paths. Prefer:
  - structured logging that only includes non-sensitive fields
  - redaction helpers that reduce URLs to `origin` (or scheme-only for non-hierarchical schemes)
  - narrowing what `Error` details are included

Example (origin-only URL logging):
```ts
function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin;
  } catch {
    return "<invalid url>";
  }
}

Logger.info(`Opening browser: ${redactUrlForLog(requestUrl)}`);
```

4) Avoid silent credential/authority precedence
- If multiple credential sources exist (OAuth vs pasted API key; CLI vs UI), ensure the intended source wins and stale credentials/tokens can’t silently override the new one.

5) Avoid silent capability/ownership fallbacks
- Capability routing/transfer should be explicit and compatibility-checked. If the intended owner is disconnected/detached, fail clearly (and emit telemetry) rather than selecting an arbitrary registrant.

These practices prevent common high-impact classes of security regressions: auth bypass via “fail open”, privilege escalation via overly broad filesystem grants, and credential exfiltration via logs/telemetry.