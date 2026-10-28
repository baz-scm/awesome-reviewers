---
title: Prevent credential leakage in logs
description: 'Treat every log line, error message, and telemetry payload as something
  a user may paste into a public bug report, and design accordingly. URLs, error messages,
  and process metadata routinely carry secrets: OAuth codes, state/nonce values, API
  keys embedded in query strings or path segments, basic-auth userinfo (`user:pass@host`),
  and quoted input from...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70986
---

Treat every log line, error message, and telemetry payload as something a user may paste into a public bug report, and design accordingly. URLs, error messages, and process metadata routinely carry secrets: OAuth codes, state/nonce values, API keys embedded in query strings or path segments, basic-auth userinfo (`user:pass@host`), and quoted input from parser errors (e.g. `JSON.parse` echoing `"sk-live-..." is not valid JSON`). Full command-line arguments of other processes can leak secrets passed as flags.

Apply these rules:
- When a URL must appear in a log, reduce it to `origin` (scheme + host + port) only. Never log the path, query string, or fragment — they routinely carry tokens, codes, or keys. For non-hierarchical schemes (`mailto:`, `data:`), keep only the scheme.
- Prefer fixing the leak at its source rather than building a generic free-text scrubber: a blocklist regex over arbitrary error text is inherently incomplete (schemeless URLs, bearer tokens, keys embedded without a recognizable URL shape will always slip through). If a call site builds an error message from a secret, fix that call site to echo the unexpanded/placeholder form instead (e.g. keep `${env:VAR}` placeholders rather than the resolved secret value).
- Give known leak-prone error shapes special handling by type, not by call site: for example, treat `SyntaxError` (including nested in a `cause` chain) as unsafe to echo in production logs — log only its name, since JSON/URL parsers quote the offending input back into the message.
- In production builds, keep log formatting narrow: only error messages (never stacks or other properties), numbers, and booleans should be serialized; drop raw strings and objects, since they routinely carry file/terminal contents or settings.
- When collecting diagnostic info about external processes (e.g. identifying a port occupant), prefer process name/executable path over full command line, since command-line arguments can contain secrets.
- Scrub sensitive environment variables from `process.env` as soon as they are read/claimed, before spawning any child process, so they cannot propagate further than necessary.

Example:
```ts
export function redactUrlForLog(url: string): string {
	try {
		const parsed = new URL(url);
		if (parsed.origin === "null") {
			return `${parsed.protocol}<redacted>`; // mailto:, data:, file:, ...
		}
		return parsed.origin; // never path, query, or fragment
	} catch {
		return "<invalid url>";
	}
}
```