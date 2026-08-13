---
title: Treat Inputs as Untrusted
description: 'Apply a consistent security posture to every workflow/prompt-controlled
  value and to any derived content that will be rendered or linked:


  1) Validate untrusted paths *before* cleanup/normalization'
repository: bmad-code-org/bmad-method
label: Security
language: Markdown
comments_count: 5
repository_stars: 51859
---

Apply a consistent security posture to every workflow/prompt-controlled value and to any derived content that will be rendered or linked:

1) Validate untrusted paths *before* cleanup/normalization
- Reject absolute paths and path traversal on the raw input first.
- Example policy: fail if input is empty, whitespace-only, contains `..`, starts with `/` or a drive letter, etc.

2) Normalize/whitelist paths before template substitution
- Strip known prefixes, normalize separators, and remove leading slashes so templates can’t be steered to unexpected files.

3) Sanitize/escape anything injected into HTML (especially attributes)
- Enforce an allowlist for external links (e.g., `http`/`https` only).
- HTML-escape URLs and all source-derived text placed into HTML attributes.
- If a value fails policy, render it as plain text.

4) Redact sensitive identifiers from generated reports/logs
- Never include usernames, handles, emails, or identifying links in artifacts/memlogs.

Minimal example (HTML + URL allowlist + escaping):
```js
function sanitizeUrlForHtml(url) {
  const u = String(url).trim();
  if (!/^https?:\/\//i.test(u)) return null;
  return u;
}

function escapeHtmlAttr(s) {
  return String(s)
    .replaceAll('&','&amp;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#39;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;');
}

const safeUrl = sanitizeUrlForHtml(sourceUrl);
const label = escapeHtmlAttr(sourceLabel);
if (safeUrl) {
  html += `<a href="${escapeHtmlAttr(safeUrl)}">[${label}]</a>`;
} else {
  html += `${label}`;
}
```

Rule of thumb: if a value comes from prompts, user/community text, filesystem paths, or external sources, assume it can be adversarial until you (a) validate/whitelist it for the target context, (b) normalize it before templating, and (c) escape it for the final rendering context.