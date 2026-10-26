---
title: Fail-Closed Security Boundaries
description: When a security boundary can be crossed (auth callbacks, capability ownership,
  filesystem access, sandbox writable grants, or logging), default to **fail-closed**,
  validate the boundary with **strong constraints**, and apply **secret-safe handling**.
repository: cline/cline#v14
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70876
---

When a security boundary can be crossed (auth callbacks, capability ownership, filesystem access, sandbox writable grants, or logging), default to **fail-closed**, validate the boundary with **strong constraints**, and apply **secret-safe handling**.

**Rules**
1. **Anti-forgery / auth verification is allow-list only**
   - If verification fails (e.g., state mismatch), proceed *only* on an explicit affirmative user action.
   - Treat “dismiss/undefined/close/esc” as **no**; do not “fall through”.

   ```ts
   if (authService.authNonce !== state) {
     const userConfirmation = await vscode.window.showWarningMessage(
       `Authentication could not be verified. Store the token from ${uri.path}?`,
       { modal: true },
       "Store"
     );
     if (userConfirmation !== "Store") return; // fail-closed
   }
   // safe to continue
   ```

2. **No silent fallback across trust boundaries**
   - For capability routing/ownership (or similar “who is allowed to act” logic), avoid implicit fallbacks like “pick first attached registrant”.
   - If ownership can’t be verified (disconnect/detach), **fail** with a clear, trackable error rather than replaying or transferring behavior.

3. **Constrain filesystem/sandbox boundaries and fail closed**
   - Workspace roots and writable grants are security boundaries:
     - Resolve/normalize paths and reject escapes.
     - For sandbox “read-write” grants (e.g., cwd/home), verify the real resolved path and reject dangerous roots/ancestors/volumes; fail closed with a user-safe message.

4. **Secret-safe logging is policy-driven**
   - In production, do not log stacks, error objects, arbitrary strings/JSON, or URLs containing sensitive data.
   - Redact URLs to at least `origin` (and never include query/fragment/userinfo).

   ```ts
   export function redactUrlForLog(url: string): string {
     try {
       const u = new URL(url);
       return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin;
     } catch {
       return "<invalid url>";
     }
   }

   Logger.info(`Opening endpoint: ${redactUrlForLog(endpointUrl)}`);
   ```

5. **When you need diagnostics, log non-sensitive detail at debug level**
   - Redact credential-bearing content in user-facing/error paths.
   - If you must capture stderr for debugging, ensure it is redacted before logging (or log it only under safe debug telemetry rules).

Adopting this standard prevents the most common security regressions shown here: auth checks that fail open, implicit capability takeovers, path/sandbox escapes, and sensitive leakage via logs/error messages.