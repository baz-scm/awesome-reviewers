---
title: Prevent hardcoded secrets
description: Never store sensitive information such as API keys, passwords, tokens,
  or credentials directly in your source code. These hardcoded secrets are easily
  exposed through version control systems, code sharing, or security breaches, creating
  significant security vulnerabilities.
repository: supabase/supabase
label: Security
language: TypeScript
comments_count: 6
repository_stars: 86070
---

Never store sensitive information such as API keys, passwords, tokens, or credentials directly in your source code. These hardcoded secrets are easily exposed through version control systems, code sharing, or security breaches, creating significant security vulnerabilities.

Instead, use:
1. Environment variables (process.env.SECRET_KEY)
2. Secret management services (AWS Secrets Manager, HashiCorp Vault)
3. Configuration files excluded from version control

For client-side applications, consider using server-side proxies to make authenticated requests rather than exposing secrets to the client.

Example of unsafe code:
```typescript
// UNSAFE: Hardcoded secrets directly in code
export const authConfig = {
  twilio_auth_token: "a9b8c7d6e5f4g3h2i1",
  aws_secret_access_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
};
```

Secure approach:
```typescript
// BETTER: Using environment variables
export const authConfig = {
  twilio_auth_token: process.env.TWILIO_AUTH_TOKEN,
  aws_secret_access_key: process.env.AWS_SECRET_ACCESS_KEY
};

// For configuration schemas, use descriptive labels without values
export const authFieldLabels = {
  sms_twilio_auth_token: "Twilio Auth Token",
  aws_secret_access_key: "AWS Secret Access Key"
};
```