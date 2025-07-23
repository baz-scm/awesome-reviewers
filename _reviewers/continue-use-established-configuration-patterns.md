---
title: Use established configuration patterns
description: Always access and set configuration values using established patterns
  and correct property names. Understanding the structure of configuration objects
  is essential to prevent bugs in your application.
repository: continuedev/continue
label: Configurations
language: TSX
comments_count: 3
repository_stars: 27819
---

Always access and set configuration values using established patterns and correct property names. Understanding the structure of configuration objects is essential to prevent bugs in your application.

When working with external services:
- Use the appropriate property names that reflect the actual configuration structure (e.g., `underlyingProviderName` instead of `provider` for services behind proxies)

When handling persistent configurations:
- Leverage existing utility functions rather than direct access methods
- Follow team conventions for localStorage access

When setting conditional configuration values:
- Ensure your logic correctly handles all possible cases
- Carefully review boolean flag assignments

```typescript
// Incorrect
if (defaultModel?.provider === "anthropic") { ... }
const storedId = localStorage.getItem("lastSessionId");
const alwaysApply = newRuleType !== RuleType.AgentRequested;

// Correct
if (defaultModel?.underlyingProviderName === "anthropic") { ... }
const storedId = getLocalStorage("lastSessionId");
const alwaysApply = newRuleType === RuleType.Always || newRuleType === RuleType.AutoAttached;
```