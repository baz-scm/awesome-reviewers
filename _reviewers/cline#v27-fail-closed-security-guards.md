---
title: Fail Closed Security Guards
description: 'Security-sensitive code must *fail closed* (never continue on ambiguous
  user/provider/client state) and must *never leak secrets* via logs.


  Apply these rules:'
repository: cline/cline#v27
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70892
---

Security-sensitive code must *fail closed* (never continue on ambiguous user/provider/client state) and must *never leak secrets* via logs.

Apply these rules:
1. **CSRF/anti-forgery checks must be strict**
   - If verification fails (e.g., state/nonce mismatch), only proceed on an explicit allowed action.
   - Treat `undefined` (dismissed prompt) as **not allowed**.

   ```ts
   // Fail-closed state mismatch handling
   if (authService.authNonce !== state) {
     const result = await vscode.window.showWarningMessage(
       `Authentication could not be verified. Store the token returned from ${uri.path}?`,
       { modal: true },
       "Store",
     );
     if (result !== "Store") return;
   }
   ```

2. **Capability/ownership transfer must be explicit**
   - Never “pick the first attached registrant” for a capability with the same name; it can silently change task behavior.
   - If the intended owner disappears, either: (a) require an explicit compatible takeover contract, or (b) fail the request with a clear message/event.

3. **Containment and sandbox grants must be bounded**
   - When computing read/write roots for sandboxes or file browsing, fail if any write grant becomes the filesystem root, a home/ancestor that effectively grants broad write access, or otherwise breaks the intended boundary.

4. **Secret-safe logging**
   - In production, only log non-secret primitives for “extra args”; never log error strings that may embed URLs/tokens.
   - Reduce logged URLs to `origin` (or redact entirely) so paths/query/callback codes/credentials aren’t exposed.
   - Fix at the source (avoid constructing secret-bearing messages at call sites); don’t rely on trying to make regex scrubbing perfect.

This standard prevents the two most damaging classes shown in the discussions: **(a) fail-open auth/state/capability behavior** and **(b) accidental secret disclosure through logs.**