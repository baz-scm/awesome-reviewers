---
title: Prevent credential leakage in logs
description: Treat every log line, error message, and bug-report artifact as potentially
  public, and design logging to never surface secrets rather than trying to scrub
  them after the fact. URLs routinely carry credentials via userinfo, query strings,
  or path segments (OAuth codes, API keys, reset tokens); parse errors can echo raw
  input (e.g. `JSON.parse` quoting the...
repository: cline/cline#|sleep 4
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70979
---

Treat every log line, error message, and bug-report artifact as potentially public, and design logging to never surface secrets rather than trying to scrub them after the fact. URLs routinely carry credentials via userinfo, query strings, or path segments (OAuth codes, API keys, reset tokens); parse errors can echo raw input (e.g. `JSON.parse` quoting the invalid text); and stack traces or object dumps can carry file contents, settings, or tokens.

Prefer fixing leaks at the source instead of building a generic scrubber: a free-text blocklist regex for "URL-like" or "secret-like" patterns always misses a shape (schemeless URLs, bearer tokens, plain-text keys), so don't rely on one as the primary defense. Instead:
- When constructing an error message, never interpolate a value that could be sensitive (e.g. build messages from the URL as the user typed it, not an env-expanded/resolved form).
- When a URL must appear in a log, reduce it to a safe subset (origin only, or origin+pathname if the path is known-safe) rather than echoing it verbatim:

```ts
function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url)
    if (parsed.origin === "null") return `${parsed.protocol}<redacted>`
    return parsed.origin
  } catch {
    return "<invalid url>"
  }
}
```
- In production logging utilities, narrow by default: only pass through primitives (numbers/booleans) and well-known-safe error properties (e.g. `name` for `SyntaxError`, since its `message` can embed parsed input); drop raw strings/objects/stacks unless running in a verbose/dev build.
- Apply the same rule to filename/path-based sensitive-data checks (e.g. credential file lists like `.netrc`, `.aws/credentials`): acknowledge they only catch known filenames, not arbitrary file contents, and don't present them as complete protection.

Document the trust boundary explicitly in code comments so later contributors don't assume a scrubber provides more protection than it does, and add regression tests asserting that known leak-prone inputs (env-expanded URLs, parse-error echoes, credentialed URLs) are not present in the rendered log output.