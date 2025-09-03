---
title: Follow documentation standards
description: Ensure all documentation follows established patterns and standards for
  components, formatting, and code examples. This includes using proper imports for
  documentation components (like Image imports instead of markdown syntax) and maintaining
  consistent formatting for code samples with standardized attributes.
repository: BerriAI/litellm
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 28310
---

Ensure all documentation follows established patterns and standards for components, formatting, and code examples. This includes using proper imports for documentation components (like Image imports instead of markdown syntax) and maintaining consistent formatting for code samples with standardized attributes.

For images, use the proper component import:
```javascript
import Image from '@theme/IdealImage';
// Use: <Image src="path/to/image.png" alt="Description" />
// Instead of: ![Description](path/to/image.png)
```

For code examples, include standard formatting attributes:
```python
# Code samples should have showLineNumbers and title
```

Always reference existing documentation examples as templates to maintain consistency across the codebase. This ensures a professional appearance and better user experience while preventing technical rendering issues.