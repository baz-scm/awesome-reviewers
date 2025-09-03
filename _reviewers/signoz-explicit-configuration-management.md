---
title: Explicit configuration management
description: Configuration changes should be intentional, well-documented, and implemented
  using clean, understandable patterns. Avoid hacky workarounds like counter-based
  state management when simpler alternatives exist.
repository: SigNoz/signoz
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 23369
---

Configuration changes should be intentional, well-documented, and implemented using clean, understandable patterns. Avoid hacky workarounds like counter-based state management when simpler alternatives exist.

When modifying configuration defaults or synchronization logic:
1. Ensure changes are intentional with clear reasoning
2. Use straightforward implementation patterns (e.g., boolean flags instead of counters)
3. Document the purpose and scope of configuration changes

Example of good practice:
```typescript
// Clear, intentional configuration change
latency_pointer: 'end', // Default to 'end' for all steps except the 1st step

// Prefer clean boolean-based synchronization
const [needsResync, setNeedsResync] = useState(false);
// Instead of hacky counter-based approach
const [reSync, setReSync] = useState(0);
```

This ensures configuration management remains maintainable and the intent behind changes is preserved for future developers.