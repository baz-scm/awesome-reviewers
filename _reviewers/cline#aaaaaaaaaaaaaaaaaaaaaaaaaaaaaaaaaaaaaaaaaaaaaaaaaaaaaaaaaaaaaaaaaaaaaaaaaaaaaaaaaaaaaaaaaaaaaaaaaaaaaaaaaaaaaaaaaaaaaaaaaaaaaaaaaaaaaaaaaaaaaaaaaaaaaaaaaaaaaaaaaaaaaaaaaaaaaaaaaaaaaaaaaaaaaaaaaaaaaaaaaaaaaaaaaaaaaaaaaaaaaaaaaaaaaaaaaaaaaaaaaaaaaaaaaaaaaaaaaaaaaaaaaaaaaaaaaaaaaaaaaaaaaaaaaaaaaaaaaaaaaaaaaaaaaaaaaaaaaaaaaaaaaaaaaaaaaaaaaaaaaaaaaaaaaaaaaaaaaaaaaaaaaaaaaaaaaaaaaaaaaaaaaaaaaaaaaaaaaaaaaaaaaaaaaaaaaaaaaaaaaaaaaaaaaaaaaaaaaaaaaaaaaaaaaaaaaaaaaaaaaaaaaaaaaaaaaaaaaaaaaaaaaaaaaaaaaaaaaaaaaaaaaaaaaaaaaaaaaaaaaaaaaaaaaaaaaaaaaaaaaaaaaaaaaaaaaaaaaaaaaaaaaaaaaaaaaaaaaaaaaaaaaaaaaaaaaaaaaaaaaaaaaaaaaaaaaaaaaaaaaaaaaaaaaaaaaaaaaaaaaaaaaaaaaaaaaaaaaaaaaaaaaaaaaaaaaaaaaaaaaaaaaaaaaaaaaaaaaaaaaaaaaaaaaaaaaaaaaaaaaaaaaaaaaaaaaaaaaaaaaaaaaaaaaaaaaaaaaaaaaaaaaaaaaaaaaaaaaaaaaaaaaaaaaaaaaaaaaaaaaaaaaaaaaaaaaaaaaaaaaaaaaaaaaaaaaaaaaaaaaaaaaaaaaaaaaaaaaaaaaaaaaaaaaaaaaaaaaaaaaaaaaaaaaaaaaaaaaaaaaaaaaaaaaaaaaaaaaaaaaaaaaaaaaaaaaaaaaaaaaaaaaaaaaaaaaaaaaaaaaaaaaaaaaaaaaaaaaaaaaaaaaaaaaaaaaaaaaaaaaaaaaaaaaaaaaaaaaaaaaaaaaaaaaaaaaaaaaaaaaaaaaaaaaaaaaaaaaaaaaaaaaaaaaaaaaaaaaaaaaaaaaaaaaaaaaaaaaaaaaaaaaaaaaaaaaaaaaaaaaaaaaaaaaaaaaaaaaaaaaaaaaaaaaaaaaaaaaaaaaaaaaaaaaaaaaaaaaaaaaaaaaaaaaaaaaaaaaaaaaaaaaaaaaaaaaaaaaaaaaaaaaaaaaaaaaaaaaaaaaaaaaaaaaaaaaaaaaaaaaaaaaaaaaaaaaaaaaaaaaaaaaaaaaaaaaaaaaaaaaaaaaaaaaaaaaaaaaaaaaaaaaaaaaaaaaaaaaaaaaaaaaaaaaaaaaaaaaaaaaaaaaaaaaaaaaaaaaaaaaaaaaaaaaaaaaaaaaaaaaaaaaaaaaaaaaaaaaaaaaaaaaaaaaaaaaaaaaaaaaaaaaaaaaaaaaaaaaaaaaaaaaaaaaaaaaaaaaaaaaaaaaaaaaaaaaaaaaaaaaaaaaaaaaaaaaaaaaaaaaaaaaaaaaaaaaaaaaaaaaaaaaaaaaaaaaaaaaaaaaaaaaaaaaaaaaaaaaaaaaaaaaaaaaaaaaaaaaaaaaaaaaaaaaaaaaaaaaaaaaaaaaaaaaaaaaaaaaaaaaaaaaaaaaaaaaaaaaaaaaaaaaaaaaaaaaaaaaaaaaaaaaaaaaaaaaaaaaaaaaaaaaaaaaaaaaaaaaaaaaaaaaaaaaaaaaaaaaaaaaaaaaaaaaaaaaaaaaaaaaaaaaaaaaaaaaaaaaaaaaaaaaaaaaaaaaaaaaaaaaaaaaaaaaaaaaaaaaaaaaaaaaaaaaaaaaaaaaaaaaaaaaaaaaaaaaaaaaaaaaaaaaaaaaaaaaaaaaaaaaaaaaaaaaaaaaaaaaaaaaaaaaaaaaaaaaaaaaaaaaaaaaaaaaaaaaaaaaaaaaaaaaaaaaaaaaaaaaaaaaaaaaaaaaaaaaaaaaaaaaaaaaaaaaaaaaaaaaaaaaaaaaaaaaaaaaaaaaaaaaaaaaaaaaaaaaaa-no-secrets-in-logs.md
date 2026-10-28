---
title: No secrets in logs
description: 'Treat every log line, error message, and diagnostic payload as something
  a user may paste into a public bug report, and assume URLs, parsed input, and subprocess
  details routinely carry credentials: OAuth codes/state, tokens, API keys embedded
  in a path or query string, `user:pass@` userinfo, or raw settings/file content echoed
  by a parser error (e.g....'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70973
---

Treat every log line, error message, and diagnostic payload as something a user may paste into a public bug report, and assume URLs, parsed input, and subprocess details routinely carry credentials: OAuth codes/state, tokens, API keys embedded in a path or query string, `user:pass@` userinfo, or raw settings/file content echoed by a parser error (e.g. `JSON.parse` quoting the offending text, which can be an API key).

Fix leaks at the source rather than trying to scrub arbitrary free text after the fact — a blocklist regex for "looks like a secret" is inherently incomplete (schemeless URLs, bearer tokens, plain-text keys always find a new shape). Concretely:
- When building an error or log message from untrusted/credential-bearing input, echo the input as the user typed it (e.g. with `${env:...}` placeholders intact) rather than an expanded/resolved value that may contain the resolved secret.
- When a URL must appear in a log, reduce it to its origin only (scheme + host + port). Strip path, query string, fragment, and userinfo — these routinely carry auth codes, reset tokens, state, or API keys passed as a path segment.
- When logging subprocess/diagnostic info (e.g. identifying what holds a port), prefer process name/executable path over full command-line arguments, since arguments can contain secrets.
- Special-case known-leaky exception types by type rather than per call site (e.g. in production, a `SyntaxError`, including one found in a `cause` chain, should log only its name/type, never its message).
- In production builds, give extra log arguments the same trust level as the message itself: numbers/booleans are safe to log verbatim, but strings and objects are routinely unsafe and should be dropped or reduced (origin-only, type-only) unless the call site has already redacted them.

Example:
```ts
// Bad: echoes the resolved URL, which may contain a credential
throw new Error(`Invalid MCP server URL: ${expandedUrl}`)

// Good: echoes what the user entered, placeholders intact
throw new Error(`Invalid MCP server URL: ${rawUrlWithPlaceholders}`)

// Good: reduce any URL that must be logged to its origin
Logger.info(`Opening browser: ${new URL(url).origin}`)
```
Apply this standard any time new code logs an error, a URL, parsed/validated input, or external process details.</description>
</invoke>
