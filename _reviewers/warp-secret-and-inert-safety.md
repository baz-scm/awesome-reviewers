---
title: Secret and Inert Safety
description: When handling auth secrets, user directory/path-based configuration,
  or shell-generated code, treat any value that could reveal identity/organization
  or execute code as *sensitive* and *untrusted by default*.
repository: warpdotdev/warp
label: Security
language: Markdown
comments_count: 4
repository_stars: 56893
---

When handling auth secrets, user directory/path-based configuration, or shell-generated code, treat any value that could reveal identity/organization or execute code as *sensitive* and *untrusted by default*.

Apply these rules:

1) Define trust boundaries explicitly
- Secret-backed and command-backed values must be treated as inert data during Drive sync/preview/import/shared browsing/metadata rendering.
- Execute or substitute into a live shell session only after explicit user action (e.g., apply/export) and only for content the user owns or has explicitly chosen to trust.

2) Escape/serialize as data, never as code
- For shell code generation (e.g., Nushell): embed dynamic values using the shell-specific literal serializer/escaping contract (double-quoted literal rules, escaping of quotes/backslashes/control chars, and correct string/argument handling).
- Never construct executable snippets by concatenating raw dynamic strings. Prefer binding escaped literals to variables and passing them as arguments.

3) Redact sensitive logs and diagnostics
- Never log raw directory/path keys, secret-manager commands, or secret stdout/stderr.
- For path-derived keys (like directory override maps), log only a stable short redacted identifier (hash) plus non-sensitive value text when needed.

4) Don’t “silently weaken” authorization scopes
- If secrets are personal-scoped by default, ensure the system cleanly supports broader scopes only when explicitly modeled (e.g., team API keys) and never by accident.

Example patterns

A) Redacted warning message (path-key privacy)
```rust
fn warn_directory_override(key: &str, theme: &str) {
  let redacted = redacted_key_id(key); // stable short id; never reversible without a local salt
  log::warn!(
    "directory_overrides[hash={}] : unknown theme '{}' — skipping this entry until corrected",
    redacted,
    theme
  );
}
```

B) Inert secret/command snippets in untrusted flows
- During sync/preview/import: store the *structured reference* (or escaped literal placeholders) but do not persist rendered secret-manager commands or secret output.
- Only after user applies/exports into an owned/trusted execution context, render/execute and keep failure output free of secrets.

Enforcement checklist / tests
- Add tests that assert:
  - Logs/telemetry never contain raw sensitive strings (raw directory keys; rendered secret-manager command; secret output).
  - Shell-generated code treats dynamic values as literals (malicious strings with quotes/$()/'/newlines stay single-statement data).
  - Secret-backed values remain inert through preview/import until explicit apply.
  - Auth-secret scope changes are authorization-driven (no accidental escalation from defaults).