---
title: Fail Closed Security Boundaries
description: 'Treat security-sensitive operations as strict boundaries: validate integrity/ownership,
  contain filesystem access with real resolved paths, and never leak credentials in
  logs.'
repository: cline/cline#v28
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70892
---

Treat security-sensitive operations as strict boundaries: validate integrity/ownership, contain filesystem access with real resolved paths, and never leak credentials in logs.

**1) Auth callback / token storage**
- Never “accept anyway” on a failed CSRF/state check by default.
- If you require user confirmation, make it explicit and modal, and proceed only on an allow-listed button value; do not store tokens on dismiss/esc.
- Ensure the nonce/state you compare is actually anti-forgery (short-lived/rotated), not a session-lifetime constant.

```ts
// Safe pattern: state mismatch must default to cancel and never store tokens.
if (authService.authNonce !== state) {
	const choice = await vscode.window.showWarningMessage(
		`Could not verify the authentication response. Store token from ${uri.path}?`,
		{ modal: true },
		"Store",
		"Cancel",
	);
	if (choice !== "Store") return; // dismiss/esc/cancel => fail closed
}
// Only now store token
if (token) await authService.storeToken(token);
```

**2) Ownership/authority transfers**
- Don’t silently pick an arbitrary compatible client/registrant for a capability takeover.
- If the original owner disconnected/detached/cancelled, fail clearly and emit telemetry to diagnose frequency.

**3) Sandboxing and filesystem containment**
- When granting read/write, resolve the real path and fail closed if it’s a volume root, home directory, or an ancestor/root of the allowed scope.
- For write APIs, only allow writes to an explicit allow-list of file types inside allowed roots; prevent symlink/`..` escapes via resolved paths.

**4) Secret-safe logging**
- In production, log only what’s necessary (e.g., error message/type, numbers/booleans) and avoid logging arbitrary strings/objects.
- Redact URLs for logs (keep only origin; never include path/query/userinfo containing tokens/codes). Don’t build error messages by concatenating credential-bearing inputs.

**Checklist for PR authors**
- [ ] Any auth/state mismatch: fail closed; no token persistence on dismiss.
- [ ] Any capability/ownership transfer: explicit compatibility contract; no silent fallback.
- [ ] Any sandbox grant/write: validate resolved real paths; deny roots/home/ancestors.
- [ ] Any logs/errors: redact URLs and do not serialize secret-bearing strings/objects in production.