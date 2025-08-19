---
title: Verify HTML escaping
description: Always verify that user-controlled content in templates is properly HTML-escaped
  to prevent XSS attacks. Don't just assume framework defaults are working - actively
  test with potentially malicious input to confirm that HTML tags are rendered as
  text rather than executed.
repository: PostHog/posthog
label: Security
language: Html
comments_count: 1
repository_stars: 28460
---

Always verify that user-controlled content in templates is properly HTML-escaped to prevent XSS attacks. Don't just assume framework defaults are working - actively test with potentially malicious input to confirm that HTML tags are rendered as text rather than executed.

When displaying dynamic content in templates, test with HTML payloads like `<img src=x />` or `<script>alert('xss')</script>` to ensure they appear as literal text. For Django templates, confirm that the standard `{{ variable }}` syntax properly escapes HTML characters, converting `<` to `&lt;`, `>` to `&gt;`, etc.

Example verification:
```html
<!-- Template: -->
<p>API Key: <strong>{{ more_info }}</strong></p>

<!-- Test input: more_info = "<img src=x />" -->
<!-- Expected output: API Key: <strong>&lt;img src=x /&gt;</strong> -->
<!-- NOT: API Key: <strong><img src=x /></strong> -->
```

This practice helps catch cases where unsafe rendering methods might be accidentally used or where framework protections might not apply.