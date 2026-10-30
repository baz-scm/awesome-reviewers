---
title: Redact secrets in logs
description: 'Logs, error messages, and bug reports routinely end up pasted publicly,
  so any value written to a log must be treated as potentially public. URLs are a
  common leak vector: query strings and fragments carry OAuth state, authorization
  codes, device codes, and reset tokens; paths can carry API keys (some MCP servers
  embed a key as a path segment); userinfo can...'
repository: cline/cline#"><b>zze3729958
label: Security
language: TypeScript
comments_count: 5
repository_stars: 71067
---

Logs, error messages, and bug reports routinely end up pasted publicly, so any value written to a log must be treated as potentially public. URLs are a common leak vector: query strings and fragments carry OAuth state, authorization codes, device codes, and reset tokens; paths can carry API keys (some MCP servers embed a key as a path segment); userinfo can carry credentials. Before logging or displaying a URL, reduce it to `origin` (or just the scheme for non-hierarchical schemes like `mailto:`/`data:`), never echo the full URL or an expanded value:

```ts
export function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url)
    if (parsed.origin === "null") return `${parsed.protocol}<redacted>`
    return parsed.origin
  } catch {
    return "<invalid url>"
  }
}
```

The same caution applies to error messages and arbitrary log arguments: runtime JSON/parse errors (`SyntaxError`) and similar built-ins routinely quote the offending input verbatim, so a malformed settings file or API response can leak a raw credential into a log line. Don't try to pattern-match and strip every possible secret shape after the fact — that's a blocklist and there's always another shape (schemeless URLs, bearer tokens, plain-text keys). Instead:
- In production builds, default log formatting to an explicit allowlist of safe types (numbers, booleans, error names) and drop strings/objects/stacks by default; reserve full serialization for verbose/development logging.
- Fix the root cause at the call site that builds a message out of a secret (e.g. echo user-supplied values like a configured URL exactly as entered, with placeholders, rather than an expanded/resolved value that may contain a token).
- When a specific error type is known to echo sensitive input (e.g. `SyntaxError`), special-case it to log only safe metadata (e.g. the error name) rather than the full message, including when it appears in a `cause` chain.

Add regression tests for redaction/formatting behavior so a future log statement or URL change can't silently regress exposure.