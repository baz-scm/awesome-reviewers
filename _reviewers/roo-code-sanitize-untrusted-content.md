---
title: Sanitize untrusted content
description: Always sanitize user-generated or externally sourced content before rendering
  it to prevent Cross-Site Scripting (XSS) vulnerabilities. Never use `dangerouslySetInnerHTML`
  with unsanitized content.
repository: RooCodeInc/Roo-Code
label: Security
language: TSX
comments_count: 3
repository_stars: 17288
---

Always sanitize user-generated or externally sourced content before rendering it to prevent Cross-Site Scripting (XSS) vulnerabilities. Never use `dangerouslySetInnerHTML` with unsanitized content.

When handling user input or external data:
1. Use a trusted HTML sanitization library (such as DOMPurify)
2. Validate and sanitize URLs before rendering images or links
3. Consider alternative rendering methods that don't require raw HTML injection

**Bad practice:**
```tsx
// Dangerous - susceptible to XSS attacks
const renderTableCell = (content: string) => {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
};
```

**Good practice:**
```tsx
import DOMPurify from 'dompurify';

// Safe - content is sanitized before rendering
const renderTableCell = (content: string) => {
  if (needsHtmlRendering(content)) {
    const sanitizedContent = DOMPurify.sanitize(content);
    return <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />;
  }
  return <span>{content}</span>;
};

// For image URLs
const renderImage = (imageUrl: string) => {
  const sanitizedUrl = sanitizeImageUrl(imageUrl);
  // Skip rendering if URL is invalid/unsafe
  if (!sanitizedUrl) {
    return null;
  }
  return <img src={sanitizedUrl} alt="User content" />;
};
```