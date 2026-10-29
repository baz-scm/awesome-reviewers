---
title: Validate and protect untrusted input
description: Any value that is user-controllable or comes from external input (request
  data, generated class names, file paths, redirect targets, header values, cookie
  options) must be treated as untrusted before it reaches a security-sensitive sink
  such as HTML/CSS output, the filesystem, or a security header/attribute.
repository: honojs/Hono
label: Security
language: TypeScript
comments_count: 8
repository_stars: 32741
---

Any value that is user-controllable or comes from external input (request data, generated class names, file paths, redirect targets, header values, cookie options) must be treated as untrusted before it reaches a security-sensitive sink such as HTML/CSS output, the filesystem, or a security header/attribute.

1. Escape or allow-list before output. When interpolating dynamic strings into HTML or CSS, always escape them (e.g. use the `html` template helper) or restrict them to a safe character set instead of emitting them as-is:
```ts
// Prefer a strict allow-list over trusting the raw value
const safeSlug = classNameSlug.replace(/[^a-zA-Z0-9_-]/g, '')

// Escape dynamic content injected into HTML
const html = `<title>Redirecting to: ${html`${to}`}</title>`
```

2. Normalize and validate file paths defensively. Strip *all* leading slashes/dots (not just one), and be careful with URL-based normalization since it can resolve encoded traversal sequences (`%2e%2e`) in unexpected ways. Add explicit guards against paths that escape the intended root:
```ts
// Strip repeated leading slashes/backslashes, not just a single one
filename = filename.replace(/^\.?[\/\\]+/, '')

// Reject paths that escape a relative root
if (root[0] !== '/' && path[0] === '/') {
  return
}
```

3. Never let user-supplied options silently weaken mandatory security attributes. When merging option objects, ensure the security-mandated fields (e.g. `secure`, `path`, `domain` for `__Secure-`/`__Host-` cookie prefixes) are applied *after* the spread of user options so they cannot be overridden:
```ts
serialize('__Host-' + name, value, { ...opt, secure: true, path: '/', domain: undefined })
```

Apply this pattern consistently: identify every place where external/user input flows into HTML, CSS, headers, paths, or security-critical options, and add explicit escaping, allow-listing, or override protection rather than trusting the input as-is.</description>
