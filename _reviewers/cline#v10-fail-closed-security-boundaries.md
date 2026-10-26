---
title: Fail-Closed Security Boundaries
description: 'Treat authorization/authentication and isolation boundaries as *fail-closed*:
  never fall back to a weaker interpretation, and never accept or route work without
  explicitly verified compatibility. Also assume secrets may appear in inputs/errors/URLs
  and ensure logging is secret-safe.'
repository: cline/cline#v10
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70869
---

Treat authorization/authentication and isolation boundaries as *fail-closed*: never fall back to a weaker interpretation, and never accept or route work without explicitly verified compatibility. Also assume secrets may appear in inputs/errors/URLs and ensure logging is secret-safe.

Apply these rules:
1) **Auth callbacks: enforce verification, don’t rely on UI dismissal**
   - If a callback fails verification (e.g., state/nonce mismatch), only proceed on an explicit allow-list user action (e.g., a specific button label with `{ modal: true }`), and prefer restoring the original hard reject.

   Example:
   ```ts
   if (authService.authNonce !== state) {
     const choice = await vscode.window.showWarningMessage(
       "Authentication could not be verified. Continue?",
       { modal: true },
       "Continue"
     );
     if (choice !== "Continue") return;
   }
   // continue only after explicit verification/choice
   ```

2) **Capability / ownership routing: no silent takeover**
   - If the intended owner disconnects/detaches, fail clearly (optionally with an actionable user message) instead of selecting “the first attached registrant”. Emit structured events with the reason for observability.

3) **Isolation/sandbox boundaries: validate the *effective* grant scope**
   - Resolve real paths and ensure your read-write grants cannot expand to filesystem roots, home directories, or unsafe ancestors. If the resolved scope is too broad, fail closed with a clear error.

   Example (pattern):
   ```ts
   const resolved = await fs.promises.realpath(cwd);
   if (isAncestor(resolved, homeDir) || isVolumeOrRoot(resolved)) {
     throw new Error("Unsafe sandbox grant: refuse to run");
   }
   ```

4) **Secret-safe logging: redact URLs and narrow production log data**
   - Never log full URLs that may contain OAuth codes/tokens, credentials in userinfo, or sensitive paths.
   - Prefer origin-only (or scheme-only for non-hierarchical schemes) for production logs.

   Example:
   ```ts
   export function redactUrlForLog(url: string): string {
     try {
       const u = new URL(url);
       if (u.origin === "null") return `${u.protocol}<redacted>`;
       return u.origin; // omit path/query/fragment
     } catch {
       return "<invalid url>";
     }
   }
   ```

5) **Treat error messages like logs**
   - If an error message is constructed from untrusted or potentially secret-bearing values, it can leak the same way as logs. Don’t embed secrets in `Error.message`; sanitize upstream or avoid including secrets entirely.

Outcome: fewer CSRF/auth bypasses, no unintended capability transfers, safer sandboxing, and dramatically reduced credential/token leakage via logs/telemetry.