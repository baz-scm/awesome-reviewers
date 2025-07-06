---
title: Use appropriate comment syntax
description: Choose the correct comment syntax based on the file type and processing
  system to ensure documentation serves its intended purpose. For template files (like
  Jinja), use template-specific comments rather than HTML comments to prevent documentation
  from appearing in rendered output. Always include explanatory comments for files
  that might seem unnecessary but...
repository: boto/boto3
label: Documentation
language: Html
comments_count: 2
repository_stars: 9417
---

Choose the correct comment syntax based on the file type and processing system to ensure documentation serves its intended purpose. For template files (like Jinja), use template-specific comments rather than HTML comments to prevent documentation from appearing in rendered output. Always include explanatory comments for files that might seem unnecessary but serve a specific purpose.

For example, in a Jinja template file:

```html
{# 
  DO NOT REMOVE THIS FILE

  This file is normally inherited from the version defined by our docs theme.
  However, that file includes in-line styling which isn't allowed by our website's
  Content Security Policy (CSP). This empty file overwrites the template inherited
  from the theme.
#}
```

Instead of:

```html
<!-- 
  DO NOT REMOVE THIS FILE
  ...explanation...
-->
```

This ensures maintenance documentation remains visible to developers but doesn't leak into generated artifacts seen by end users.