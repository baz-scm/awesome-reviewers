---
title: Optimize store selectors
description: Write store selectors with proper patterns to prevent unnecessary component
  re-renders. Use inline selector functions that extract only the needed data, and
  provide custom equality comparisons for complex data types like arrays and objects.
repository: lobehub/lobe-chat
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 65138
---

Write store selectors with proper patterns to prevent unnecessary component re-renders. Use inline selector functions that extract only the needed data, and provide custom equality comparisons for complex data types like arrays and objects.

For simple value extraction, use inline selector functions:
```ts
// ❌ Incorrect - causes re-renders when unrelated store data changes
const config = useAgentStore(agentChatConfigSelectors.currentChatConfig);
const enableCompressHistory = config.enableCompressHistory;

// ✅ Correct - only re-renders when enableCompressHistory changes
const enableCompressHistory = useAgentStore(
  s => agentChatConfigSelectors.currentChatConfig(s).enableCompressHistory
);
```

For arrays and objects, use equality comparisons to prevent re-renders on reference changes:
```ts
import isEqual from 'fast-deep-equal';

// ✅ Correct - prevents re-renders when array contents are the same
const remoteModels = useUserStore(
  modelProviderSelectors.remoteProviderModelCards(provider), 
  isEqual
);
```

This prevents performance issues where components re-render unnecessarily when unrelated store data changes, improving overall application responsiveness.