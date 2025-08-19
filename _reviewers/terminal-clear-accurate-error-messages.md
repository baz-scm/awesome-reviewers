---
title: Clear accurate error messages
description: Error messages should be clear, accurate, and contextually appropriate
  to help users understand what went wrong and how to fix it. Use complete, descriptive
  terms instead of abbreviations or technical jargon that may confuse users. Ensure
  error messages accurately reflect the actual capabilities and constraints of the
  system rather than copying generic...
repository: microsoft/terminal
label: Error Handling
language: Other
comments_count: 3
repository_stars: 99242
---

Error messages should be clear, accurate, and contextually appropriate to help users understand what went wrong and how to fix it. Use complete, descriptive terms instead of abbreviations or technical jargon that may confuse users. Ensure error messages accurately reflect the actual capabilities and constraints of the system rather than copying generic messages that may not apply.

Key principles:
- Use full descriptive terms (e.g., "regular expression" instead of "regex")
- Ensure messages match actual system capabilities (don't mention features that aren't supported)
- Make error conditions explicit rather than silently falling back to default behavior
- Test error scenarios to verify message accuracy

Example from the discussions:
```xml
<!-- Better: Clear and complete terminology -->
<value>An invalid regular expression was found.</value>

<!-- Avoid: Abbreviated or potentially misleading terms -->
<value>An invalid regex was found.</value>
```

When encountering unhandled cases, consider using explicit error detection (like assertions) rather than returning empty or default values that mask the underlying problem.