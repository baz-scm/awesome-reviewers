---
title: Prevent secret leakage in logs
description: 'Treat every log line, error message, and telemetry payload as potentially
  public: they end up in output channels, bug reports users paste publicly, or metrics
  pipelines. Default to redacting or omitting any data that can carry credentials,
  tokens, or other sensitive values, rather than trying to maintain a blocklist of
  "dangerous" shapes (schemeless URLs,...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70964
---

Treat every log line, error message, and telemetry payload as potentially public: they end up in output channels, bug reports users paste publicly, or metrics pipelines. Default to redacting or omitting any data that can carry credentials, tokens, or other sensitive values, rather than trying to maintain a blocklist of "dangerous" shapes (schemeless URLs, bearer tokens, plaintext keys always find a new shape).

Concretely:
- When logging a URL, reduce it to just the origin (or scheme for non-hierarchical URLs). Query strings, fragments, paths, and userinfo routinely carry OAuth state, auth codes, device codes, reset tokens, or API keys embedded as path segments:
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
- In production builds, narrow what extra log arguments are allowed to carry: only error messages (never stacks or other error properties), numbers, and booleans. Drop strings/objects by default, since they routinely carry file/terminal contents, settings, or secrets.
- Watch for runtime-generated error messages that echo raw input, e.g. `JSON.parse` quoting the offending text (`Unexpected token 's', "sk-live-…" is not valid JSON`). Scrub by error type (e.g. log only `SyntaxError`'s name) rather than patching every call site that might parse sensitive input.
- Never forward a child process's full command line/arguments into logs or telemetry when diagnosing what holds a resource (e.g. a port); collect only non-sensitive identifying fields (process name, executable path) instead of `CommandLine`.
- When introducing or extending lists of "sensitive" filenames/fields to protect (secrets files, credential-bearing settings keys), treat them as best-effort and keep extending coverage as new channels are discovered — e.g. a credential can live in a custom header, not just an `apiKey` field, so credential-detection logic must be updated whenever a new place to store credentials is added. Document explicitly that filename/field-based checks are not a substitute for content-based secret scanning.
- At the source, never construct a log or error string by interpolating a raw secret-bearing value; pass the identifying, non-sensitive parts instead (e.g. echo a configured URL with `${env:…}` placeholders rather than its expanded value).

Add or extend a regression test whenever a new leak channel is fixed so the specific case (a URL with credentials, a JSON parse error containing a key, a header carrying a token) stays caught.</description>
</invoke>
