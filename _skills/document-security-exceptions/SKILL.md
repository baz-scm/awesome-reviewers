---
name: document-security-exceptions
description: When disabling security-related linter rules or bypassing security best
  practices, always include comments that explain why the exception is necessary,
  why it remains secure, and link to relevant security policies. This creates an audit
  trail and ensures future developers understand the security implications.
version: '1.0'
---
# Document security exceptions

When disabling security-related linter rules or bypassing security best practices, always include comments that explain why the exception is necessary, why it remains secure, and link to relevant security policies. This creates an audit trail and ensures future developers understand the security implications.

Example:
```tsx
/* eslint-disable react/iframe-missing-sandbox */
// Exception justified: This iframe only loads content from our AuthManager 
// which is part of the deployment and considered trusted per our security policy:
// https://airflow.apache.org/docs/apache-airflow/stable/security/security_model.html
<iframe src={trustedSource} title="Auth content" />
```
