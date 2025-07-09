---
title: Sanitize external content
description: Always sanitize and validate external content before processing or rendering
  it to prevent security vulnerabilities like XSS (Cross-Site Scripting) and injection
  attacks. This applies to HTML content from emails, user inputs, URL parameters,
  and any data from untrusted sources.
repository: elie222/inbox-zero
label: Security
language: TSX
comments_count: 3
repository_stars: 8267
---

Always sanitize and validate external content before processing or rendering it to prevent security vulnerabilities like XSS (Cross-Site Scripting) and injection attacks. This applies to HTML content from emails, user inputs, URL parameters, and any data from untrusted sources.

For HTML content:
```javascript
import DOMPurify from "dompurify";

// When displaying HTML content
export function HtmlEmail({ html }: { html: string }) {
  const srcDoc = useMemo(() => {
    try {
      const sanitizedHtml = DOMPurify.sanitize(html);
      return getIframeHtml(sanitizedHtml);
    } catch (error) {
      console.error("Failed to process HTML:", error);
      return "<p>Failed to load email content</p>";
    }
  }, [html]);
  // Rest of component...
}

// When converting text to HTML
const nudgeHtml = nudge
  ? nudge
      .split("\n")
      .filter((line) => line.trim())
      .map((line) => `<p>${DOMPurify.sanitize(line)}</p>`)
      .join("")
  : "";
```

For URL parameters:
```javascript
// Instead of string concatenation:
// const url = `/api/endpoint?param=${value}&other=${otherValue}`;

// Use URLSearchParams to properly encode parameters
const url = `/api/endpoint?${new URLSearchParams({
  param: value,
  other: otherValue,
})}`;
```

This approach prevents malicious code execution, data theft, session hijacking, and other security vulnerabilities that can arise from improperly handled external content.