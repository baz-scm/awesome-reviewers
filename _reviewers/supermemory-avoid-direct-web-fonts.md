---
title: Avoid direct web fonts
description: In security-sensitive or privileged contexts like browser extensions,
  avoid directly loading fonts (or other static assets) from arbitrary remote URLs
  at runtime. Remote loading can break due to CORS and may create long-term reliability/security-review
  issues.
repository: supermemoryai/supermemory
label: Security
language: Other
comments_count: 1
repository_stars: 28844
---

In security-sensitive or privileged contexts like browser extensions, avoid directly loading fonts (or other static assets) from arbitrary remote URLs at runtime. Remote loading can break due to CORS and may create long-term reliability/security-review issues.

Do this instead:
- Bundle the font asset with the extension and load it via extension-local URLs.
- Ensure your extension’s CSP allows only the required local sources.

Example (bundle locally, don’t fetch remote):
- Place `SpaceGrotesk-Bold.ttf` in your extension assets.
- Reference it using an extension URL (conceptually):

```js
// content script / extension code
const fontUrl = chrome.runtime.getURL('fonts/SpaceGrotesk-Bold.ttf');

// then use in CSS (e.g., injected stylesheet)
const css = `@font-face { font-family: 'Space Grotesk'; src: url('${fontUrl}') format('truetype'); font-weight: 700; }`;
```

If a remote font is truly required, treat it as a security dependency: enforce HTTPS, validate sources, confirm CORS behavior, and ensure your CSP and extension review requirements are satisfied.