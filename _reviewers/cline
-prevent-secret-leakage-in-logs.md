---
title: Prevent secret leakage in logs
description: Never try to keep secrets out of logs, error messages, or diagnostic
  output by blocklisting or scrubbing arbitrary free text — URLs, file paths, command
  lines, and parser error messages can all carry credentials (OAuth codes/state, API
  keys, tokens, `user:pass@` userinfo, device codes), and there is always another
  shape of secret a blocklist will miss....
repository: 'cline/cline

  '
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70942
---

Never try to keep secrets out of logs, error messages, or diagnostic output by blocklisting or scrubbing arbitrary free text — URLs, file paths, command lines, and parser error messages can all carry credentials (OAuth codes/state, API keys, tokens, `user:pass@` userinfo, device codes), and there is always another shape of secret a blocklist will miss. Instead:

1. Fix the leak at the source. Code that builds a log line or error message must not embed secret-bearing values into it. For example, when echoing a user-supplied URL back (e.g. in an MCP server config), preserve `${env:...}` placeholders rather than the expanded value.
2. When a value that *could* carry secrets must be logged (URLs, raw process info, parsed file contents), reduce it to a narrow, explicit allowlist of safe fields rather than passing it through or trying to strip the unsafe parts:
   - URLs: log only `origin` (drop path, query, fragment, and userinfo), e.g.
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
   - Error objects whose message can echo raw input (e.g. `JSON.parse` `SyntaxError`, including inside a `cause` chain): log only the error name/type in production, not the message or stack.
   - External process/listener info: log process name and executable path only, never full command-line arguments.
3. Apply this consistently across build modes — a "verbose/debug" log path is not exempt just because it's less visible; assume debug output and bug-report-pasted logs are equally public.
4. This same reasoning extends beyond logging: filename- or pattern-based blocklists for detecting sensitive files (`.netrc`, `.aws/credentials`, etc.) catch known cases but cannot catch arbitrary file contents (e.g. a credential JSON under an innocuous name) — treat such lists as a partial mitigation and say so in comments/docs rather than presenting them as complete protection.

Add regression tests for any redaction/allowlist logic to lock in the safe behavior.