---
title: Clear security error messages
description: When implementing security restrictions or policies, ensure error messages
  clearly explain what the security boundary is, why it exists, and what specifically
  triggered the violation. Vague or technical jargon can leave developers confused
  about security requirements.
repository: cypress-io/cypress
label: Security
language: Other
comments_count: 1
repository_stars: 48850
---

When implementing security restrictions or policies, ensure error messages clearly explain what the security boundary is, why it exists, and what specifically triggered the violation. Vague or technical jargon can leave developers confused about security requirements.

Security error messages should include:
- The specific policy or restriction that was violated
- What action triggered the security error
- Clear explanation of the security boundary (e.g., origin policy, authentication requirements)
- Reference to relevant documentation when the concept is complex

Example of improvement:
```
// Before: Vague message
"A cross origin error happens when your application navigates to a new superdomain"

// After: Clear and specific
"A cross origin error happens when your application navigates to a new domain which does not match the origin policy above.
Cypress does not allow you to navigate to different origin within a single test.
An origin is defined by protocol + host + port."
```

This approach helps developers understand security constraints and work within them effectively, rather than being blocked by cryptic error messages.