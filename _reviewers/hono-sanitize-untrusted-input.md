---
title: Sanitize untrusted input
description: 'Treat any value derived from user input (headers, paths, query/form
  data, or option strings) as untrusted whenever it flows into HTML output, CSS output,
  regex construction, file-path resolution, or security-critical attributes. Concretely:'
repository: honojs/hono
label: Security
language: TypeScript
comments_count: 5
repository_stars: 32741
---

Treat any value derived from user input (headers, paths, query/form data, or option strings) as untrusted whenever it flows into HTML output, CSS output, regex construction, file-path resolution, or security-critical attributes. Concretely:

- When interpolating user-controlled values into HTML, always escape them (e.g. use the `html` template helper) instead of concatenating raw strings, even for "unlikely" inputs like redirect targets.
- When user-controlled values become CSS class names or other CSS tokens, restrict them to a safe character set (e.g. `[a-zA-Z0-9_-]`) rather than attempting to escape them, to avoid breaking out of the attribute/selector context.
- When building regular expressions from user-supplied separators or tokens (e.g. splitting header values), avoid patterns prone to catastrophic backtracking (ReDoS). Prefer simple `split()` + `trim()` over complex whitespace regexes like `/\s*,\s*/`.
- When resolving file paths from request input, normalize leading slashes/dots defensively (e.g. collapse repeated leading slashes with `/^\.?[\/\\]+/`) and explicitly guard against path traversal when combining a relative `root` with a user-supplied path — reject the result if it would resolve outside the intended root.
- When implementing security-relevant features with "secure-by-default" attributes (e.g. cookie `__Secure-`/`__Host-` prefixes requiring `secure: true`, `path: '/'`, no `domain`), do not let caller-supplied options silently override these mandated attributes; apply caller options first, then enforce the required security attributes last.

Add targeted tests for the malicious/edge-case inputs (e.g. script payloads in redirect targets, `///etc/passwd`-style paths, malformed class names) alongside the fix.