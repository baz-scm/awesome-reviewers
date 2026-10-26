---
title: Redact secrets in diagnostics
description: Never let credentials, tokens, or other sensitive values reach logs,
  error messages, or telemetry, even indirectly. URLs commonly carry secrets in userinfo
  (`user:pass@host`), query strings (OAuth codes, state, device codes), or even path
  segments (some MCP servers embed API keys there); when logging a URL, reduce it
  to `origin` (or `protocol` for...
repository: cline/cline
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70886
---

Never let credentials, tokens, or other sensitive values reach logs, error messages, or telemetry, even indirectly. URLs commonly carry secrets in userinfo (`user:pass@host`), query strings (OAuth codes, state, device codes), or even path segments (some MCP servers embed API keys there); when logging a URL, reduce it to `origin` (or `protocol` for non-hierarchical schemes) rather than echoing it whole:

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

The same caution applies beyond URLs: never log raw `stderr`/process output (can contain paths, remotes, or embedded credentials), never log a subprocess's command-line arguments (collect executable name/path only, not full `CommandLine`), and strip query strings/credentials from git remotes and similar identifiers before they leave the machine. When a value only needs to be used for correlation/telemetry (e.g. a workspace or session id derived from a path), derive it with a keyed hash (HMAC with a random, non-exported, non-persisted secret) instead of a plain hash or the raw value, so the identifier can't be reversed or correlated outside the current process lifetime.

Prefer fixing the leak at its source (the call site that builds the error/log message) over building a generic, blanket scrubber for arbitrary free-text log arguments — blocklist-based scrubbing of arbitrary text is inherently incomplete (schemeless URLs, bearer tokens, plain-text keys will always slip through new call sites). Expanding filename/pattern-based sensitive-file detection (e.g. `.netrc`, `.pgpass`, `.aws/credentials`, `*.keystore`) is useful for file-transfer or upload paths, but treat it as defense in depth, not a substitute for sanitizing at the point of capture.