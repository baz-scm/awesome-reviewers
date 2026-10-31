---
title: Redact secrets from logs
description: Treat any free-form string that might reach a log, error message, telemetry
  payload, or diagnostic report as a potential carrier of credentials — URLs (query
  strings, fragments, path segments, and userinfo routinely hold OAuth state, auth
  codes, tokens, or API keys), error messages (e.g. `JSON.parse` quotes the raw input
  it failed on), full command...
repository: cline/cline?foo=bar
label: Security
language: TypeScript
comments_count: 8
repository_stars: 71082
---

Treat any free-form string that might reach a log, error message, telemetry payload, or diagnostic report as a potential carrier of credentials — URLs (query strings, fragments, path segments, and userinfo routinely hold OAuth state, auth codes, tokens, or API keys), error messages (e.g. `JSON.parse` quotes the raw input it failed on), full command lines/argv of other processes, environment variables, and raw file contents. Default to a strict allowlist of what is safe to emit rather than a blocklist that strips "known" secret shapes, since a blocklist always misses the next one (schemeless URLs, bearer tokens, keys in plain text). In production paths:

- Reduce URLs to `origin` only before logging (drop path, query, fragment, userinfo); for non-hierarchical schemes keep just the scheme (`mailto:<redacted>`).
- When matching URLs embedded in free text, anchor the match to real URL syntax and stop only at whitespace/quotes/angle-brackets — not at parentheses or brackets, which are valid URL characters and would leak the remainder.
- Log only an error's name/type by default, not its message or stack, unless the call site guarantees the message is secret-free (e.g. the error type itself — `SyntaxError` — is a stronger signal than any call-site allowlist).
- When inspecting another process (e.g. for a port/resource conflict), collect only identifying fields such as executable name/path — never full command-line arguments.
- Scrub credential-bearing environment variables from `process.env` as soon as they're read and before any child process is spawned.
- Prefer filename/extension-based detection for known credential file types (`.netrc`, `.pgpass`, `.aws/credentials`, `*.pem`, `*.keystore`, etc.) when scanning for sensitive files to exclude, but document that this is best-effort and does not catch secrets in arbitrarily named files — don't present it as comprehensive scanning.
- Cover every redaction path with tests for edge cases: URLs inside parentheses/brackets, IPv6 hosts, userinfo credentials, and non-standard schemes.

Example:
```ts
function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url)
    if (parsed.origin === "null") return `${parsed.protocol}<redacted>`
    return parsed.origin // never path/query/fragment/userinfo
  } catch {
    return "<invalid url>"
  }
}
```