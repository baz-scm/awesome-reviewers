---
title: Security Invariants Guardrails
description: 'When changing auth/secret/TLS/validation code, treat existing security
  semantics as invariants: refactors must not weaken them, and config defaults/warnings
  must be applied after schema normalization.'
repository: apache/apisix
label: Security
language: Other
comments_count: 9
repository_stars: 16922
---

When changing auth/secret/TLS/validation code, treat existing security semantics as invariants: refactors must not weaken them, and config defaults/warnings must be applied after schema normalization.

Apply this checklist:
1) Preserve security-critical behavior (anti-spoofing / header clearing / response withholding)
- Keep the original “remove/clear” semantics when an upstream auth response does not contain a header. Do not replace unconditional logic with guards that allow client-injected values.

Example (anti-spoofing header clearing):
```lua
-- Security invariant: headers not present in auth response must not survive
for _, header in ipairs(conf.upstream_headers) do
    local header_value = res.headers[header]
    -- keep old behavior: nil clears any client-supplied header
    core.request.set_header(ctx, header, header_value)
end
```

2) Ensure fail-open/fail-closed is explicit and testable
- If a guard/plugin withholds output until the “assembled” payload is available, handle missing telemetry/events deterministically; never silently release data due to absent optional signals.
- Add regression tests for missing chunks/events and for the intended open/closed behavior.

3) Encrypt sensitive fields at rest (and verify framework support)
- Add `encrypt_fields` for every secret stored in plugin metadata/config.
- If a secret-ref mechanism bypasses schema constraints, ensure the remaining protections (required fields, allowed formats, dependency checks) still hold.

4) TLS verification warnings/config must reflect reality
- Expose `tls.verify` (default true) and emit warnings using the established helper, placed after schema defaults are applied so `{}` is handled as expected.
- Don’t rely on options that are silently ignored by the HTTP client; document the required CA/trust configuration so TLS verification works with default in-cluster settings.

5) Secret-manager integration must load required config in all subsystems
- If secrets are resolved in stream/worker paths, ensure the init/snapshot preload covers the necessary etcd directories; add coverage for both HTTP and stream secret references.

This prevents common production failures: header spoofing regressions, silent fail-open in guards, plaintext secret persistence, missing/incorrect TLS verification warnings, and secret-resolution breakage due to incomplete preload/config coverage.