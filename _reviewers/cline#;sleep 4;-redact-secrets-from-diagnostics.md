---
title: Redact secrets from diagnostics
description: Treat any data that can carry credentials, tokens, or auth codes as unsafe
  to log, telemetry, or persist verbatim. URLs routinely carry secrets in userinfo,
  query strings (OAuth state/codes, device codes, reset tokens), and even path segments
  (some MCP servers embed API keys as a path segment); process listings can carry
  secrets in command-line arguments;...
repository: cline/cline#;sleep 4;
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70976
---

Treat any data that can carry credentials, tokens, or auth codes as unsafe to log, telemetry, or persist verbatim. URLs routinely carry secrets in userinfo, query strings (OAuth state/codes, device codes, reset tokens), and even path segments (some MCP servers embed API keys as a path segment); process listings can carry secrets in command-line arguments; and ad-hoc "helpful" debug text built from user/server-controlled strings can smuggle in anything. Reduce these to the minimum needed for diagnosis before they reach a log line, telemetry event, or error message:

```ts
// Reduce a URL to just its origin for logs — paths, query strings, and
// userinfo routinely carry secrets.
export function redactUrlForLog(url: string): string {
	try {
		const parsed = new URL(url);
		if (parsed.origin === "null") {
			return `${parsed.protocol}<redacted>`; // mailto:, data:, file:, ...
		}
		return parsed.origin;
	} catch {
		return "<invalid url>";
	}
}
```

Apply this pattern consistently:
- Prefer capturing structured, known-safe fields (executable name/path, origin, status code) over free-form strings (full command line, full URL, raw error text).
- Don't try to make a blocklist-based scrubber "comprehensive" for arbitrary text — there is always another shape of secret it misses (schemeless URLs, bearer tokens, keys in plain prose). Instead, fix the call site that builds a message out of a secret, since production logs any message verbatim.
- Any extra argument passed to a log/telemetry call gets the same trust as the message itself — never pass raw secrets, auth headers, or full request/response bodies as log arguments.
- If sensitive data must be persisted temporarily (draft state, recovery files, caches), tie it to the owning account/session, encrypt or restrict permissions appropriately, and give it an expiry rather than leaving it indefinitely on disk.
- When redacting is not possible (e.g., a corrupt or unreadable value), fail safely and say so explicitly in the output rather than silently dropping or echoing the raw value.