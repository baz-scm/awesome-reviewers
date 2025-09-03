---
title: Document security policy trade-offs
description: When implementing security policies like Content Security Policy (CSP),
  always include clear documentation explaining the reasoning behind each directive
  choice and any security trade-offs being made. This prevents confusion during code
  reviews and ensures team members understand the security implications.
repository: cypress-io/cypress
label: Security
language: Html
comments_count: 1
repository_stars: 48850
---

When implementing security policies like Content Security Policy (CSP), always include clear documentation explaining the reasoning behind each directive choice and any security trade-offs being made. This prevents confusion during code reviews and ensures team members understand the security implications.

For example, when using less secure CSP directives, document why they're necessary:

```html
<!--
  Using 'unsafe-inline' instead of 'self' because we need to allow inline <script> tags.
  Trade-off: 'self' would be more secure but throws errors for inline scripts.
  This configuration fixes issue #3785 without reintroducing #19697.
-->
<meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'" />
```

This practice helps maintain security awareness across the team and provides context for future modifications to security configurations.