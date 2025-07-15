---
title: "Explicit CSP nonce management"
description: "When implementing Content Security Policy (CSP) protections, always explicitly pass nonce values to components rather than auto-applying them. This gives developers more control over security aspects and prevents potential security bypasses when integrating components from different sources."
repository: "facebook/react"
label: "Security"
language: "JavaScript"
comments_count: 2
repository_stars: 237000
---

When implementing Content Security Policy (CSP) protections, always explicitly pass nonce values to components rather than auto-applying them. This gives developers more control over security aspects and prevents potential security bypasses when integrating components from different sources.

Key implementation guidelines:
- Pass nonces explicitly to components that need them (like style and script elements)
- Be aware that different content types may require different nonce values (`style-src` and `script-src` directives)
- Ensure elements with different nonces aren't inappropriately merged
- Handle nonces consistently across your application

Example in React:

```javascript
// Correct: Explicitly passing nonce to style elements
<style
  href="foo"
  precedence="default"
  nonce={CSPnonce}>{`.foo { color: hotpink; }`}</style>

// When rendering on server, pass nonce to the renderer
renderToPipeableStream(
  <App />,
  { nonce: CSPnonce }
);

// For preinitialized styles, ensure nonces are added consistently
// to maintain security guarantees
const preinitOptions = {
  precedence: 'default',
  nonce: CSPnonce // Explicitly add nonce here too
};
```

Properly implemented CSP with nonces is one of the strongest defenses against cross-site scripting (XSS) attacks, but only if nonces are managed correctly and consistently throughout your application.