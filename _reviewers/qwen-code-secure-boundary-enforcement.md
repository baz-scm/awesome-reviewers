---
title: Secure Boundary Enforcement
description: 'Standard: at every trust boundary, enforce security invariants in a
  way that cannot be skipped by flags, parsing edge cases, alternate code paths, or
  serialization differences.'
repository: QwenLM/qwen-code
label: Security
language: TypeScript
comments_count: 20
repository_stars: 26407
---

Standard: at every trust boundary, enforce security invariants in a way that cannot be skipped by flags, parsing edge cases, alternate code paths, or serialization differences.

Checklist (apply consistently):
1) Feature flags must not become bypass switches
- If you add “allow X”, still keep the security properties that prevent the class of attack (e.g., metadata SSRF). Don’t short-circuit validation after DNS/normalization; apply the invariant checks unconditionally.

2) Validate identifiers and map them safely to filesystem/network usage
- For IDs that influence paths/files: require strict format (e.g., UUID) and reject path traversal primitives (path separators, `..`, control chars).
- Ensure the accepted format at the HTTP/route boundary matches the downstream service/storage patterns, so you don’t create “orphaned” states.

Example (route boundary):
```ts
function assertSessionId(raw: unknown): string {
  if (typeof raw !== 'string') throw new Error('invalid');
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(raw))
    throw new Error('invalid');
  return raw;
}
```

3) Handle untrusted filesystem objects safely (symlinks/TOCTOU)
- Never rely on a “check then read” with `lstat`/`stat` followed by `readFile` where the path can be swapped.
- Use `open()` with `O_NOFOLLOW` (and reject non-regular via `fstat`) and enforce a size cap before reading.

4) Sanitize all outputs on every path (not just the happy path)
- Any string derived from untrusted inputs (user text, streaming markers, image markers, filenames, error messages) must be sanitized/escaped before it reaches the UI or external API.
- Audit non-primary paths like cancel/fail/early-return flows; they often bypass sanitization.

Example (cancel path must sanitize like append):
```ts
await finalize(segmentId,
  sanitizeStreamingImageMarkers(record.content),
  'Cancelled',
  false,
);
```

5) Authorization/auth token propagation must be end-to-end
- If a request requires auth, every subsequent related call must forward the token (don’t “best effort” swallow auth errors where correctness depends on authorization).

6) Confidentiality: treat platform “internal” flags as security labels
- If an upstream note/comment is marked internal/confidential, ensure both ingestion filtering and the reply path preserve the confidentiality (e.g., reply should be internal or not sent publicly).

7) Parsing/regex guards must be robust to escape and grammar edge cases
- Don’t assume string-matching is sufficient for security-sensitive parsing (shell operators, destructive-command patterns). Prefer structural parsing or grammar-aware checks; if regex is used, it must be escape-aware and tested against adversarial separators.

8) Enforce sender-policy and consistent untrusted-data framing before aggregation
- When batching multiple authors/messages into one envelope, apply sender-policy per item before aggregation; don’t decide authorization based on the first element.
- Ensure the “untrusted data” framing appears in the model-facing `text` consistently across lanes and first-contact paths.

9) Don’t trust carriers written by the audited execution
- For any “tripwire/audit” mechanism, ensure the audit boundary is stored outside the attacker’s write authority or cryptographically/procedurally verified; otherwise the audited code can forge the carrier to make the audit report falsely clean.

This standard is meant to be a practical code-review rubric: when you see “allow/skip/early return/regex parse/check-then-use”, require that the security invariant still holds and that untrusted data cannot reach sinks (filesystem paths, network endpoints, subprocess argv, UI/LLM text, or public replies) without the corresponding validation/sanitization/authorization guarantees.