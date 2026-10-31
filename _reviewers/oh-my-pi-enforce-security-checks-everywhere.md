---
title: Enforce security checks everywhere
description: Security-sensitive logic—credential/secret redaction, data-scope isolation,
  authorization/allowlist matching, and output sanitization—must be enforced on every
  code path that can reach the sensitive data or untrusted input, not just the common
  or first-discovered path. Audit all entry points (alternate parsers, fallback branches,
  defaults, display paths)...
repository: can1357/oh-my-pi
label: Security
language: TypeScript
comments_count: 9
repository_stars: 37317
---

Security-sensitive logic—credential/secret redaction, data-scope isolation, authorization/allowlist matching, and output sanitization—must be enforced on every code path that can reach the sensitive data or untrusted input, not just the common or first-discovered path. Audit all entry points (alternate parsers, fallback branches, defaults, display paths) for the same guarantee before shipping, and add a regression test per bypass path.

Recurring failure patterns to check for:
- Redaction/sanitization applied on one branch but skipped on another (e.g. a `data:` URI decode path that returns before text-based credential scrubbing runs, or ANSI/control characters stripped in the wide-layout render but not the narrow/truncated one).
- An "exemption" or default meant for one narrow context (e.g. VS Code predefined variables) applied globally, silently defeating validation for unrelated contexts (e.g. an HTTP header `Authorization: Bearer ${workspaceFolder}` in a non-VS-Code config passes through unflagged).
- Authorization/allowlist matching that is too permissive: a provider-scoped glob (`openai/*`) matching a bare model id regardless of provider (`openrouter/openai/gpt-5`), or an unconfigured role still granting access via a fallback/chain lookup instead of being rejected outright.
- Data scoped to one boundary (session, tenant) being persisted or replicated with a wider/default scope by a secondary write path (e.g. a session-scoped fact ending up stored with `scope='global'` because a graph-ingestion or extraction path didn't thread the source scope through), leaking data across the boundary.
- Approval/consent decisions made on a different payload than what is actually executed (e.g. stripping a parameter before an approval hook sees it, then restoring it for execution), breaking the audit/approval guarantee.

When adding a new path that touches sensitive data (new storage writer, new input decoder, new matcher, new display renderer), explicitly verify it goes through the same sanitization/scoping/authorization function as existing paths—don't duplicate or special-case the logic—and add a test that exercises the bypass scenario (e.g. a credential embedded in a base64 data URI, a session-scoped fact recalled from another session, a disallowed provider id matching an allowlist glob) to prevent regressions.