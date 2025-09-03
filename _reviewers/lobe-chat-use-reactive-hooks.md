---
title: Use reactive hooks
description: Always use React's reactive hook patterns instead of imperative state
  access or manual effect management. This ensures proper component re-rendering,
  better performance, and cleaner code architecture.
repository: lobehub/lobe-chat
label: React
language: TSX
comments_count: 4
repository_stars: 65138
---

Always use React's reactive hook patterns instead of imperative state access or manual effect management. This ensures proper component re-rendering, better performance, and cleaner code architecture.

**Avoid non-reactive state access:**
```ts
// ❌ Bad - non-reactive, fixed value
const config = useAgentStore.getState().currentAgentChatConfig;
const inboxMessages = useChatStore.getState().messagesMap[messageMapKey(INBOX_SESSION_ID, activeTopicId)] || [];

// ✅ Good - reactive hook usage
const config = useAgentStore(agentSelectors.currentAgentChatConfig);
const inboxMessages = useChatStore(chatSelectors.inboxActiveTopicMessages);
```

**Use proper data fetching patterns:**
```ts
// ❌ Bad - manual useEffect for data fetching
useEffect(() => {
  const fetchData = async () => {
    const data = await api.getData();
    setData(data);
  };
  fetchData();
}, []);

// ✅ Good - use data fetching libraries
const { data, loading, error } = useSWR('/api/data', fetcher);
```

**Leverage React's built-in capabilities:**
- Use built-in form synchronization instead of manual useEffect for form updates
- Create reusable selectors to avoid component re-renders and improve code reusability
- Prefer declarative patterns that work with React's rendering cycle rather than imperative workarounds