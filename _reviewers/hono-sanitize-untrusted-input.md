---
title: Sanitize untrusted input
description: Any value that comes from the client or another external source (headers,
  query params, path segments, class names, cookie values, etc.) must be validated,
  escaped, or restricted to a known-safe set before it is used in a context where
  it can change the meaning of surrounding code — dynamic `RegExp` construction, HTML/attribute
  output, or file-system path...
repository: HONOJS/HONO
label: Security
language: TypeScript
comments_count: 7
repository_stars: 32741
---

Any value that comes from the client or another external source (headers, query params, path segments, class names, cookie values, etc.) must be validated, escaped, or restricted to a known-safe set before it is used in a context where it can change the meaning of surrounding code — dynamic `RegExp` construction, HTML/attribute output, or file-system path resolution.

- Dynamic RegExp: never interpolate raw user input into a `RegExp`. Escape metacharacters first, and avoid patterns prone to catastrophic backtracking (e.g. `/\s*,\s*/`); prefer a simple `split(',').map(s => s.trim())` instead.
- HTML output: never build HTML via raw template literals with untrusted values. Use the project's escaping helper, e.g. ``${html`${to}`}``, so injected markup/scripts can't execute.
- Identifiers emitted into CSS/HTML (e.g. generated class names): don't try to escape after the fact — restrict the allowed input to a safe character set such as `[a-zA-Z0-9_-]` up front.
- Finite-domain inputs (e.g. `Sec-Fetch-Site` values): model them as a closed TypeScript union/allow-list and validate at runtime with a type guard instead of accepting an open `string`.
- File paths derived from request input: normalize and verify the resolved path cannot escape the configured root. Watch for encoded traversal sequences (`%2e%2e`), repeated/leading slashes, and absolute-path overrides — add an explicit "is still inside root" check in addition to normalization, since normalization alone (e.g. via `URL`) can silently resolve `..` segments in unsafe ways.

Example — safe RegExp construction:
```ts
// Bad: user-controlled prefix used unescaped in a RegExp
const prefixRegexStr = options.prefix === '' ? '' : `${options.prefix} +`

// Good: escape regex metacharacters first
const prefixRegexStr = options.prefix === '' ? '' : `${escapeRegExp(options.prefix)} +`
```

Treat every external input as hostile until it has been constrained to a safe shape for its destination context.