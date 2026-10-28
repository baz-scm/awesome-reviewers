---
title: Prevent credential exposure
description: Treat every output channel a user or support agent can see — log lines,
  error messages, bug reports, and persisted files — as public, and assume any string
  value may carry a secret (API keys, OAuth tokens/codes, session nonces, `user:pass@`
  or query-string credentials, device codes, path-embedded tokens). Don't echo raw
  strings or objects into logs/errors;...
repository: "cline/cline\r\n"
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70946
---

Treat every output channel a user or support agent can see — log lines, error messages, bug reports, and persisted files — as public, and assume any string value may carry a secret (API keys, OAuth tokens/codes, session nonces, `user:pass@` or query-string credentials, device codes, path-embedded tokens). Don't echo raw strings or objects into logs/errors; only pass through values you've explicitly classified as safe (numbers, booleans, enum-like tags, or a value you've deliberately redacted).

Apply this at the chokepoint rather than per call site:
- In logging utilities, default production builds to a narrow allow-list (numbers, booleans, error *names*, never full messages/stacks/raw objects), since native errors (e.g. `JSON.parse` SyntaxError) routinely quote the credential-bearing input they failed on.
- When logging or storing a URL, strip everything but the origin — query strings, fragments, userinfo, and even the path can carry OAuth state, auth codes, reset tokens, or an embedded API key:
```ts
export function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url)
    if (parsed.origin === "null") return `${parsed.protocol}<redacted>`
    return parsed.origin // not pathname, search, or hash
  } catch {
    return "<invalid url>"
  }
}
```
- Don't rely on a free-text scrubber to strip secrets after the fact — it's a blocklist that always misses a new shape. Fix the call site that builds the unsafe message instead (e.g. echo a URL as entered with placeholders, never the expanded/credentialed value).
- When classifying which fields are "credential-bearing" (for auth-source tracking, secret-scanning, or redaction lists), audit every channel the credential can travel through, not just the obvious field — request headers (`Authorization`, `api-key`) are as much a credential channel as `apiKey`/`aws`/`auth`.
- When persisting potentially sensitive data to disk (drafts, follow-up payloads, cached settings), prefer encryption or a short expiry and avoid writing it in plaintext indefinitely.

When you must detect "is this path/value sensitive" (e.g. refusing to push `.netrc`, `.aws/credentials`, keystores), keep the list as broad as practical, but document explicitly that filename-based checks are not comprehensive — they can't catch a credential in an arbitrarily named file — rather than presenting them as full protection.