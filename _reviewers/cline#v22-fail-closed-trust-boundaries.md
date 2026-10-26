---
title: Fail-Closed Trust Boundaries
description: 'Security-sensitive flows must be fail-closed and must not leak secrets.


  Apply these rules:

  1) Auth/callback verification is never “prompt-and-continue” unless the verification
  is positively accepted.'
repository: cline/cline#v22
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70886
---

Security-sensitive flows must be fail-closed and must not leak secrets.

Apply these rules:
1) Auth/callback verification is never “prompt-and-continue” unless the verification is positively accepted.
   - If an auth callback’s anti-forgery state/nonce is mismatched, only proceed on an explicit allow-list user action (and treat dismiss/undefined as deny).

   Example:
   ```ts
   // Fail closed on state mismatch.
   if (authService.authNonce !== state) {
     const userChoice = await vscode.window.showWarningMessage(
       "Could not verify auth callback state. Continue only if you initiated this sign-in?",
       { modal: true },
       "Store"
     );
     if (userChoice !== "Store") return;
   }
   // Only here is it safe to store the token.
   saveToken(token);
   ```
2) Ownership/capability routing must be explicit; never silently transfer or replay work to an unrelated registrant.
   - If the original capability owner is disconnected/detached, fail with a safe message and emit telemetry instead of guessing a different client.
3) Logs/errors must be production-safe against secret exfiltration.
   - In production, narrow logged values (e.g., allow only error messages + numbers/booleans; drop strings/objects).
   - Redact URLs to origin (and avoid echoing env-expanded/credential-bearing URLs or paths).
   - Call sites must not build error strings that embed secrets; redact at the source.

   Example URL redaction policy:
   ```ts
   export function redactUrlForLog(url: string): string {
     try {
       const u = new URL(url)
       return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin
     } catch {
       return "<invalid url>"
     }
   }
   ```
4) Sandbox/file permission grants must be verified with real resolved paths and fail closed for unsafe roots.
   - Before granting read-write, resolve real paths and reject grants that target home directories, filesystem roots, or volume/drive ancestors.

These changes prevent: CSRF/replay token storage on unverified callbacks, silent behavior changes via capability takeover, and credential leakage via logs/errors—while keeping sandbox boundaries trustworthy.