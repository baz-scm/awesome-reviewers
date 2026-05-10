---
title: Use Contextual Sanitization
description: Any diagram text/config that can originate from users (node labels, tooltips,
  markdown, theme/style tokens, and link targets) must be treated as untrusted. Apply
  **context-appropriate** escaping/sanitization and avoid security-by-regex.
repository: mermaid-js/mermaid
label: Security
language: TypeScript
comments_count: 7
repository_stars: 87952
---

Any diagram text/config that can originate from users (node labels, tooltips, markdown, theme/style tokens, and link targets) must be treated as untrusted. Apply **context-appropriate** escaping/sanitization and avoid security-by-regex.

Practical rules:
- **HTML insertion:** If you must use `.html(...)`, sanitize the string (e.g., `DOMPurify`/`rehype-sanitize`) and/or ensure all metacharacters are escaped. If you only need plain text, prefer `.text(...)`.
- **SVG/CSS URL tokens:** When constructing values for `url(...)` in SVG/CSS, use `CSS.escape()` (or equivalent) instead of manual `replace` chains.
- **Markdown to HTML:** Treat markdown-to-HTML as an HTML generation pipeline. Prefer a sanitize step and don’t assume “micromark is safe” means “output is safe to inject.”
- **Link targets:** Do not allow dangerous schemes like `javascript:` in any “click”/link rendering path. Add tests that ensure unsafe schemes are rejected/neutralized.
- **Validation for style/config:** For theme/style properties that become CSS (colors, sizes, weights, radii), validate formats/ranges before using them.

Example patterns:
- Plain text (safe default):
  ```ts
  tooltipEl.text(userProvidedTitle); // avoid .html for untrusted strings
  ```
- Contextual escaping for CSS URL tokens:
  ```ts
  const safeToken = CSS.escape(untrustedToken);
  const css = `url(${safeToken})`;
  ```
- Validate config inputs before using as CSS:
  ```ts
  function isValidHexColor(s: string) {
    return /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.test(s);
  }
  if (theme.primaryColor && !isValidHexColor(theme.primaryColor)) throw new Error('Invalid color');
  ```