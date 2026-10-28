---
title: Avoid leaking secrets
description: 'Treat any data that may carry credentials, tokens, or other sensitive
  values as unsafe to log, echo, or compare against an incomplete blocklist. Specifically:'
repository: cline/cline?ref=main
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70980
---

Treat any data that may carry credentials, tokens, or other sensitive values as unsafe to log, echo, or compare against an incomplete blocklist. Specifically:

- **Fix leaks at the source, not downstream with a blocklist.** Blocklist-based scrubbing of free text (filenames, error strings, command output) is inherently incomplete — there is always another shape of secret (schemeless URLs, bearer tokens, plain keys, a new sensitive filename). Prefer stopping a secret from ever entering the message in the first place over trying to strip it out later. For example, build error messages from the URL as the user entered it (with `${env:...}` placeholders intact) instead of the expanded/resolved value.
- **Reduce URLs before logging.** Query strings, fragments, path segments, and userinfo routinely carry OAuth state, auth codes, reset tokens, or API keys. When a URL must appear in a log line, reduce it to just its origin (or scheme, if non-hierarchical) rather than logging it verbatim:
```ts
export function redactUrlForLog(url: string): string {
	try {
		const parsed = new URL(url);
		if (parsed.origin === "null") return `${parsed.protocol}<redacted>`;
		return parsed.origin;
	} catch {
		return "<invalid url>";
	}
}
```
- **Don't pass raw command lines/arguments into logs or telemetry.** When shelling out to inspect another process (e.g. diagnosing a port conflict), prefer process name/executable path over full command line, since arguments can contain secrets.
- **Enumerate every channel a credential can travel through, not just the obvious field.** When tracking or clearing credentials (API keys, OAuth tokens, auth headers), audit all fields that can carry secrets — e.g. a provider's `apiKey` field, nested `aws`/`auth` objects, and custom request `headers` (some APIs accept the key via `Authorization` or `api-key` headers) — and document which fields were deliberately excluded and why.
- **Keep sensitive-file/credential checks as an explicit, documented list**, and extend it as new cases are found (e.g. `.netrc`, `.pgpass`, `.aws/credentials`, keystores), while being explicit in comments/docs about what the check does *not* catch (e.g. filename-based checks don't scan file contents for embedded secrets).

Apply this standard whenever adding logging, telemetry, diagnostics, or error messages that touch URLs, file paths, command invocations, or credential-related settings.