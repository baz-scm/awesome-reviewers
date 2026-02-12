---
title: avoid raw injection
description: When generating and inserting HTML or CSS as raw strings, treat it as
  untrusted input and avoid direct injection into the DOM. Constructing <style> tags
  or innerHTML from dynamic values can enable XSS if any part of those values is attacker-controlled.
repository: likec4/likec4
label: Security
language: TSX
comments_count: 1
repository_stars: 2582
---

When generating and inserting HTML or CSS as raw strings, treat it as untrusted input and avoid direct injection into the DOM. Constructing <style> tags or innerHTML from dynamic values can enable XSS if any part of those values is attacker-controlled.

Guidance:
- Prefer safe APIs:
  - Use React props/style or CSS variables on elements instead of creating raw <style> blocks from strings.
  - Validate and constrain any identifiers (e.g., CSS selectors, data-* attributes) and color/value formats before use.
- If you must insert raw HTML/CSS, do so explicitly and sanitize:
  - Use a well-maintained HTML/CSS sanitizer (e.g., DOMPurify for HTML) or rigorous validation for CSS values.
  - Use dangerouslySetInnerHTML only with a sanitized string and a code comment explaining why injection is necessary.
- Add code review attention and, where applicable, a unit test asserting sanitized output or allowed-value enforcement.

Examples:
// Unsafe: building a <style> string from external input (risky)
const styles = Object.entries(customColors).map(([name, color]) => `:where([data-likec4-color=${name}]) { --clr: ${color}; }`).join('\n');
return <style>{styles}</style>; // avoid this unless input is fully trusted

// Safer: set CSS variables on elements (no raw HTML injection)
// For each themed container element:
<div data-likec4-color={name} style={{ ['--likec4-color' as any]: color }} />

// If injection is required, sanitize and document
import DOMPurify from 'dompurify';
const safe = DOMPurify.sanitize(styles, {ALLOWED_TAGS: ['style'], ALLOWED_ATTR: []});
return <style dangerouslySetInnerHTML={{ __html: safe }} />; // include comment why injection is necessary

Why this matters: Unescaped or unsanitized content inserted into the DOM can enable XSS or CSS injections. Using safe APIs, validation, or vetted sanitization prevents class of security vulnerabilities and makes intent explicit during code review.