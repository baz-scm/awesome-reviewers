---
title: Effective Auth Propagation
description: 'Security-sensitive behavior must be correct *in the real execution boundary*:
  resolve the effective security configuration (including profile overrides) and then
  propagate/enforce it through packaged subprocesses and trust-boundary validations.'
repository: openai/codex-security
label: Security
language: TypeScript
comments_count: 6
repository_stars: 9394
---

Security-sensitive behavior must be correct *in the real execution boundary*: resolve the effective security configuration (including profile overrides) and then propagate/enforce it through packaged subprocesses and trust-boundary validations.

Apply this as a standard checklist:
1) Resolve effective auth/provider
- Determine the provider/auth method from the selected profile’s effective settings (not only root/top-level values).
- Use that resolved value consistently for preflight, runtime env selection, and CLI behavior.

2) Propagate credentials across boundaries with allowlists
- When delegating to bundled plugins/workers (including MCP/subprocess), ensure the packed manifest/allowlist includes the exact credential/env vars required.
- Add tests that exercise the real worker subprocess (and the packed npm artifact), not only a mocked parent-process environment.

3) Preserve explicit credential intent
- If using ambient credentials or stored homes, never overwrite an explicit login/logout state.
- Only import ambient credentials to initialize an empty credential home; preserve user logout/selection otherwise.

4) Validate trust boundaries using the correct context
- For filesystem/security checks, validate the *containing* parent/ancestors that determine replacement/rename ability—don’t stop early.
- For Windows credential homes, inspect/repair ACLs defensively (no unsafe translation), and deny/repair when ownership/trust rules can’t be proven.

5) Make secret handling deterministic and testable
- Ensure redaction/parsing logic can’t be tricked by escape/quoting ambiguity; pin behavior with regression tests.

Example pattern (effective provider + boundary allowlist):
```ts
// 1) Resolve effective provider from selected profile
const effectiveProvider = resolveProfileProvider(selectedProfile, rootConfig);
const authentication = scanAuthentication(rootConfig, authMode, effectiveProvider);

// 2) Ensure only explicitly allowlisted vars are forwarded to bundled worker
const allowedEnv = getBundledMcpEnvAllowlistForProvider(effectiveProvider);
const childEnv = Object.fromEntries(
  Object.entries(process.env).filter(([k]) => allowedEnv.has(k)),
);
spawnWorker({ env: childEnv });
```

Net effect: fewer “it passed the test but shipped unauthenticated/insecure” outcomes and more reliable security guarantees across auth selection, credential propagation, and trust-boundary enforcement.