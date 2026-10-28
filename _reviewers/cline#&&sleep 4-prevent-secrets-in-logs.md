---
title: Prevent secrets in logs
description: 'Treat every log line, error message, and bug-report-visible output as
  potentially public, and make sure credentials, tokens, and other sensitive data
  never end up in it. In particular:'
repository: cline/cline#&&sleep 4
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70980
---

Treat every log line, error message, and bug-report-visible output as potentially public, and make sure credentials, tokens, and other sensitive data never end up in it. In particular:

- Build error messages from trusted, literal data, not from values that may embed secrets. For example, construct an "invalid URL" error from the URL as the user entered it (with placeholders like `${env:...}` intact), not from an env-expanded or otherwise resolved value that could contain a credential.
- When a URL must be logged, reduce it to its origin only. Paths, query strings, fragments, and userinfo routinely carry OAuth state, authorization codes, reset/magic-link tokens, or API keys embedded as path segments; keep only scheme+host+port, and fall back to `<scheme>:<redacted>` or `<invalid url>` when the value can't be parsed.
- In production builds, keep log argument serialization narrow: only safe primitives (numbers, booleans) and vetted error representations should be printed. Never serialize arbitrary strings or objects as log arguments, since they routinely carry URLs, file/terminal contents, or settings. Extend this "same trust as the log message" rule to special error types that echo their input, e.g. `SyntaxError` from `JSON.parse`, which quotes the offending text (so a parsed API key or credential-bearing payload would otherwise leak) — collapse these to just the error name/type in production.
- Prefer fixing leaks at the call site that creates the risky message over adding a generic free-text scrubber. Blocklist-based scrubbers (regex over arbitrary text) are fragile — they will always miss some shape (schemeless URLs, bearer tokens, keys in plain text) — so the sustainable fix is ensuring the code that builds the message never embeds the secret in the first place, with the logger providing structural protections (origin-only URLs, primitive-only args, no stack traces) as a backstop, not the primary defense.
- Add regression tests for each redaction rule (e.g. URL-in-text matching that doesn't truncate at parentheses/brackets which are legal URL characters, or JSON-parse error redaction) so the policy doesn't regress silently.

Example:
```ts
// Bad: echoes an env-expanded or parsed value that may carry a secret
throw new Error(`Invalid MCP server URL: ${expandedUrl}`)

// Good: echoes the value as the user entered it
throw new Error(`Invalid MCP server URL: ${rawUrlWithPlaceholders}`)

// Good: reduce to origin before logging
Logger.info(`Opening browser: ${redactUrlForLog(url)}`)
```