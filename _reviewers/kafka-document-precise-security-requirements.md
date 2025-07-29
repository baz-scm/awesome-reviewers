---
title: Document precise security requirements
description: Security documentation must specify exact permission requirements with
  clear scope and timing details. Vague or outdated security requirements can lead
  to insufficient ACL configurations, creating security gaps or deployment failures.
repository: apache/kafka
label: Security
language: Html
comments_count: 2
repository_stars: 30575
---

Security documentation must specify exact permission requirements with clear scope and timing details. Vague or outdated security requirements can lead to insufficient ACL configurations, creating security gaps or deployment failures.

When documenting security permissions:
- Specify the exact operations required (e.g., DESCRIBE, READ, CREATE)
- Clearly define the resource scope (e.g., "all topics in the application's topology" vs "topics included in the message")
- Include timing context when permissions are needed (e.g., "when first joining")
- Keep documentation synchronized with implementation changes

Example of imprecise vs precise documentation:
```
// Imprecise - could lead to missing permissions
Required for all topics included in the message

// Precise - clear scope and timing
Required for all topics used in the application's topology, when first joining
```

Regularly review security documentation against actual implementation requirements to ensure accuracy and completeness.