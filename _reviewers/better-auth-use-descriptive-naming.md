---
title: Use descriptive naming
description: Choose specific, contextual names over generic terms to improve code
  clarity and maintainability. Generic names become ambiguous when combined into larger
  APIs or codebases, making it difficult for developers to understand functionality
  at a glance.
repository: better-auth/better-auth
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 19651
---

Choose specific, contextual names over generic terms to improve code clarity and maintainability. Generic names become ambiguous when combined into larger APIs or codebases, making it difficult for developers to understand functionality at a glance.

When naming functions, variables, or properties, include enough context to make their purpose clear without requiring additional documentation or code inspection.

**Examples of improvements:**

```typescript
// ❌ Generic, unclear in larger context
export const verify = async (input) => { ... }
// ✅ Specific, self-documenting
export const verifySiweMessage = async (input) => { ... }

// ❌ Ambiguous scope
skipConsent?: boolean;
// ✅ Clear scope and intent  
skipConsentForTrustedClients?: boolean;

// ❌ Generic endpoint naming
export const realEndpoint: TelemetryEndpoint = async (event) => { ... }
// ✅ Descriptive function naming
export const sendTelemetryEvent = async (event) => { ... }
```

This practice becomes especially important in plugin systems or large APIs where multiple modules contribute functionality under a common namespace. A name like `auth.api.verify` provides little context, while `auth.api.verifySiweMessage` immediately communicates its specific purpose.