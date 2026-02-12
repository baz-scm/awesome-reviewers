---
title: Sanitize CSS values
description: When generating CSS from external data (JSON, user input, theme files),
  validate and sanitize both CSS property names and values before injecting them into
  style elements to prevent style-breaking input and XSS/style injection.
repository: wavetermdev/waveterm
label: Security
language: TSX
comments_count: 1
repository_stars: 17328
---

When generating CSS from external data (JSON, user input, theme files), validate and sanitize both CSS property names and values before injecting them into style elements to prevent style-breaking input and XSS/style injection.

Motivation: Building CSS via string concatenation (e.g. `--term-${key}: ${value};`) can allow malicious or malformed keys/values to break the stylesheet or inject content. Use browser APIs and input validation to make this safe.

How to apply:
- Prefer CSSOM APIs instead of raw string injection: use element.style.setProperty(propertyName, value).
- Escape property names with CSS.escape when used in a context that requires serialization.
- Validate values with a whitelist or conservative regex: disallow characters that can break CSS such as `;`, `}` or HTML tag delimiters, and limit length. For colors/units consider explicit parsers or allowlists (hex colors, rgb(), numbers+units).
- If full fidelity is required, parse/serialize values using strict rules rather than passing arbitrary strings into a style element.

Example (adapted from the discussion):

// unsafe: `--term-${key}: ${value};`
// safer approach:
function isValidKey(key) {
  // allow lowercase letters, numbers, and hyphens (adjust to your naming rules)
  return /^[a-z0-9-]+$/.test(key);
}

function isValidValue(value) {
  if (typeof value !== 'string' || value.length > 200) return false;
  // disallow characters that can close or break CSS rules
  return !/[;{}<>]/.test(value);
}

async function applyTheme(themeJson, styleEl) {
  for (const [key, value] of Object.entries(themeJson)) {
    if (!isValidKey(key) || !isValidValue(String(value))) continue; // reject invalid entries

    // use CSS custom property API which avoids injecting raw CSS text
    // ensure the property name is valid per your rules
    styleEl.style.setProperty(`--term-${CSS.escape(key)}`, String(value));
  }
}

Notes:
- CSS.escape is broadly available and safe for serializing identifiers; still validate keys to match your naming expectations.
- For values that are colors or units, prefer strict parsing (e.g., validate hex, rgb(), or numeric+unit) rather than a permissive regex.
- When creating <style> text from dynamic data is unavoidable, ensure every key/value pair is validated and escaped, and avoid embedding untrusted HTML.

References: [0]