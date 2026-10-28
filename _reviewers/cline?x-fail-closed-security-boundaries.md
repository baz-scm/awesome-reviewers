---
title: Fail-closed security boundaries
description: 'Security-sensitive checks must default to deny and be conservative in
  what they allow, rather than defaulting to allow and trying to list the few things
  to reject. This applies broadly:'
repository: cline/cline?x
label: Security
language: TypeScript
comments_count: 17
repository_stars: 70983
---

Security-sensitive checks must default to deny and be conservative in what they allow, rather than defaulting to allow and trying to list the few things to reject. This applies broadly:

- **Auth/CSRF validation must actually block, not just warn.** A mismatch (e.g. OAuth state/nonce) should reject by default; only an explicit, affirmative user action should proceed. Never fall through to the "allowed" branch on an unhandled or ambiguous UI result (e.g. a dismissed dialog resolving to `undefined`). Prefer an allow-list check over a deny-list check:
```ts
// Bad: fails open if userConfirmation is undefined (dialog dismissed)
if (userConfirmation === "Cancel") return

// Good: only an explicit "Store" click proceeds
if (userConfirmation !== "Store") return
```
- **Path/boundary containment must use resolved real paths and reject any escape**, not just a prefix match on the raw string (`..` can appear as `..notes`, not just `../`). Resolve symlinks before comparing, and keep the containment logic in one shared helper rather than reimplementing it per call site.
- **Sandbox/permission grants must be minimal and explicit.** Don't grant write access to a directory without checking it isn't a drive root, volume root, or an ancestor of the home directory; don't request capabilities (e.g. network ingress) a platform doesn't need, since an unnecessary request can cause a stricter enforcement tier to fail closed entirely.
- **Authorization checks on destructive/cross-session actions should be consistent across all related commands**, not added piecemeal to only the new one.
- **Never log or persist secrets.** Redact credentials from URLs (query strings, fragments, userinfo, and paths can all carry tokens/keys), and treat any field that can carry a credential (API keys, OAuth tokens, auth headers, `.netrc`-style files, service-account JSON) as sensitive — keep the detection list broad and documented as filename/field-based rather than a false guarantee of completeness, since content-based secrets in arbitrarily named files are not caught by filename checks alone.
- **Avoid split or duplicated credential storage/paths** (e.g. a legacy field alongside the canonical one); consolidate so there is one source of truth for resolving a credential, and repair insecure file permissions (e.g. world-readable secrets files) on load.

When adding or reviewing a security-relevant check, explicitly test the "deny" path (dismissed dialogs, boundary-escaping paths, missing permissions) in addition to the intended "allow" path.