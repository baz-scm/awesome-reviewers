---
title: Prevent security vulnerabilities
description: Proactively identify and prevent common security vulnerabilities in code,
  particularly around sensitive data handling and input validation. Avoid logging
  sensitive information like API keys, tokens, or passwords that could be exposed
  in log files. Implement robust input validation using proper parsing methods rather
  than simple string operations that can be...
repository: ChatGPTNextWeb/NextChat
label: Security
language: TypeScript
comments_count: 2
repository_stars: 85721
---

Proactively identify and prevent common security vulnerabilities in code, particularly around sensitive data handling and input validation. Avoid logging sensitive information like API keys, tokens, or passwords that could be exposed in log files. Implement robust input validation using proper parsing methods rather than simple string operations that can be bypassed.

For sensitive data logging:
```typescript
// ❌ Avoid - exposes sensitive data
console.log("[Auth] use system api key", systemApiKey);

// ✅ Better - log without sensitive details  
console.log("[Auth] use system api key");
```

For input validation:
```typescript
// ❌ Avoid - can be bypassed with crafted URLs
if (!endpoint || !endpoint.endsWith("upstash.io")) {

// ✅ Better - use proper URL parsing
try {
  if (!(new URL(endpoint).hostname.endsWith('.upstash.io'))) {
    throw new Error('Invalid endpoint');
  }
} catch (e) {
  throw new Error('Invalid URL format');
}
```

Always consider how an attacker might exploit weak validation or gain access to sensitive information through logs, error messages, or other data exposure points.