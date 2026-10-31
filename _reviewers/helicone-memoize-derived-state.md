---
title: Memoize derived state
description: Avoid using `useState` + `useEffect` to compute values that can be derived
  directly from existing props, state, or query results. Filtering, mapping, formatting,
  or any other pure transformation of existing data should be wrapped in `useMemo`
  (with the correct dependency array) rather than recomputed on every render or pushed
  into local state via an effect.
repository: Helicone/helicone
label: React
language: TSX
comments_count: 9
repository_stars: 6248
---

Avoid using `useState` + `useEffect` to compute values that can be derived directly from existing props, state, or query results. Filtering, mapping, formatting, or any other pure transformation of existing data should be wrapped in `useMemo` (with the correct dependency array) rather than recomputed on every render or pushed into local state via an effect.

This matters for two reasons: performance (recomputing expensive derivations on every render) and correctness. Setting state inside a `useEffect` that also depends on that same state is a common source of infinite render loops. For example:

```tsx
// Bad: infinite loop risk — effect depends on mappedContent and also sets it
useEffect(() => {
  if (needsIds) {
    setMappedContent({ ...mappedContent, schema: { ... } });
  }
}, [mappedContent]);

// Good: derive with useMemo, no state/effect needed
const normalizedContent = useMemo(() => {
  if (!mappedContent?.schema.request?.messages) return mappedContent;
  const messages = mappedContent.schema.request.messages;
  const needsIds = messages.some((m) => !m.id);
  if (!needsIds) return mappedContent;
  return {
    ...mappedContent,
    schema: {
      ...mappedContent.schema,
      request: {
        ...mappedContent.schema.request,
        messages: messages.map((m, i) => ({ ...m, id: m.id ?? `msg-${i}-${Date.now()}` })),
      },
    },
  };
}, [mappedContent]);
```

If state truly must be updated from within an effect based on its previous value, use the functional updater form (`setState(prev => ...)`) and exclude the state itself from the dependency array to break the cycle.

The same principle applies to server/async state: prefer existing data-fetching hooks (e.g., `useQuery`/`useMutation`, or generated API hooks like `$JAWN_API.useQuery`) over manually wiring `useState` + `useEffect` to fetch and store data. This removes boilerplate, avoids stale/duplicate state, and leverages built-in caching, loading, and error handling.

```tsx
// Prefer
const { data, isLoading } = $JAWN_API.useQuery("get", "/v1/rate-limits", {}, {
  enabled: !!org?.currentOrg?.id,
});

// Over manually wrapping useQuery with a fetchFn and separate useState calls
```

Before reaching for `useState`/`useEffect`, ask whether the value can instead be computed with `useMemo` or sourced from a query hook — only fall back to state + effects for genuine side effects (subscriptions, imperative DOM/browser APIs, etc.).