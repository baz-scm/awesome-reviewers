---
title: Redact secrets from logs
description: 'Treat every log line, telemetry event, and diagnostic string as something
  a user may paste publicly, and assume any URL, command line, or parsed input passing
  through it can carry credentials. Apply these rules at the logging layer rather
  than trying to sanitize every call site:'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Security
language: TypeScript
comments_count: 5
repository_stars: 71067
---

Treat every log line, telemetry event, and diagnostic string as something a user may paste publicly, and assume any URL, command line, or parsed input passing through it can carry credentials. Apply these rules at the logging layer rather than trying to sanitize every call site:

- Never log a raw URL. Query strings, fragments, and path segments routinely carry OAuth state, auth codes, device codes, reset tokens, or API keys (some integrations embed a key as a path segment), and userinfo can carry a password. Reduce to `origin` (or `origin + pathname` only when the path itself is known-safe) before logging, and replace unparseable input entirely rather than echoing it:
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
- Never forward another process's full command line into logs/telemetry (e.g. diagnosing a port conflict). Capture only the executable name/path, not its arguments, which can contain secrets passed on the CLI.
- Don't blanket-serialize arbitrary objects/errors in production. Error stacks, raw settings objects, and other properties routinely contain file contents, tokens, or terminal output. In production, only pass through values with no room for a secret (error name, numbers, booleans) plus error messages — and hold call sites to the same rule: a message built from a secret is a bug at that call site, not something the logger can catch after the fact.
- Watch for indirect leaks: `JSON.parse` errors in V8/Bun quote the offending input in the message (e.g. `"sk-live-…" is not valid JSON`), so any parse of a credential-bearing string (settings files, API responses) can leak through a `SyntaxError`. Special-case these by error type (log only the error name) rather than patching every parse call site.
- Reserve full/verbose serialization for development-only builds; production logging must default to the narrow, redacted path described above.

This policy should be enforced centrally in the shared logging utility so new call sites inherit safe behavior by default, instead of relying on each call site to remember to redact.