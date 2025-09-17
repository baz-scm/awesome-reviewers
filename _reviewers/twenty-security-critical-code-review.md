---
title: Security-critical code review
description: Changes to security-sensitive areas like authentication, input validation,
  and business logic require extra scrutiny and thorough review. These modifications
  can introduce vulnerabilities if not properly validated.
repository: twentyhq/twenty
label: Security
language: TypeScript
comments_count: 3
repository_stars: 35477
---

Changes to security-sensitive areas like authentication, input validation, and business logic require extra scrutiny and thorough review. These modifications can introduce vulnerabilities if not properly validated.

Key areas requiring heightened security review:
- Authentication and authorization logic changes
- Input processing and data sanitization 
- Business operations that could be financially abused
- API endpoints and service layer security controls

When reviewing such changes, verify that:
- Security implications are thoroughly understood and documented
- Input validation prevents injection attacks (SQL, CSV, XSS, etc.)
- Business logic prevents abuse scenarios (e.g., credit manipulation)
- Changes don't weaken existing security controls

Example of proper input sanitization:
```typescript
// Prevent CSV injection by prefixing dangerous formulas
const sanitizedValue = value.startsWith('=') || value.startsWith('+') 
  ? `${CSV_INJECTION_PREVENTION_ZWJ}${value}` 
  : value;
```

For authentication changes, consider reverting risky modifications if the security impact cannot be clearly demonstrated as safe. As one reviewer noted: "This change is risky. What you're checking now is not the same as what was checked before."