---
title: RFC-compliant HTTP semantics
description: When implementing HTTP-level behavior—headers, charsets, content negotiation—always
  conform to the governing RFC rather than relying on internal Node.js conventions
  or convenience logic that silently changes existing semantics.
repository: Expressjs/Express
label: Networking
language: JavaScript
comments_count: 6
repository_stars: 69580
---

When implementing HTTP-level behavior—headers, charsets, content negotiation—always conform to the governing RFC rather than relying on internal Node.js conventions or convenience logic that silently changes existing semantics.

For header values, use the exact token/value required by the HTTP spec, not an internal alias. For example, Node's Buffer encoding alias `utf8` is not a valid HTTP charset token; the header must use `utf-8` per IANA's character-set registry and RFC 9110:
```js
// wrong: reuses Node's internal encoding name in the header
this.set('Content-Type', setCharset(type, encoding)); // encoding === 'utf8'

// correct: use the RFC-valid charset token for the header, keep the
// internal encoding separate
this.set('Content-Type', setCharset(type, 'utf-8'));
```
Similarly, when building structured headers like `Link`, follow the exact grammar defined by the relevant RFC (e.g., RFC 5988's `link-extension` production) for attribute names/values (token vs. quoted-string vs. extended notation) instead of ad-hoc regexes that only cover a subset of valid cases.

The same discipline applies to content-negotiation logic such as `req.accepts()`. Do not alter established negotiation semantics (e.g., treating `*/*` as an automatic match) without considering how it breaks explicit type checks consumers rely on; such policy decisions belong at the application level, not baked into the framework's spec-driven matching logic.

Before changing any HTTP-facing behavior, verify it against the applicable RFC and existing negotiation contracts, and add tests that assert the exact wire-format/semantics (e.g., assert the actual header string sent, or the negotiation result for ambiguous inputs).