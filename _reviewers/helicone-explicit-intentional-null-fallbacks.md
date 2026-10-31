---
title: Explicit, intentional null fallbacks
description: When a value may be null or undefined, don't silently coalesce it to
  a generic default without considering the semantic consequences. A careless `??
  0` or `?? "default"` can mask real errors (e.g., returning 0 for a queue size that
  failed to load, hiding an alert that should stay active) or produce incorrect behavior
  (e.g., treating a missing...
repository: Helicone/helicone
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 6248
---

When a value may be null or undefined, don't silently coalesce it to a generic default without considering the semantic consequences. A careless `?? 0` or `?? "default"` can mask real errors (e.g., returning 0 for a queue size that failed to load, hiding an alert that should stay active) or produce incorrect behavior (e.g., treating a missing `organizationId` as a shared "default" bucket instead of logging and skipping the operation). Before adding a fallback, ask whether the caller should instead explicitly handle the nullable case, log the anomaly, or propagate the absence of a value rather than papering over it.

When a fallback is genuinely appropriate, make the intent explicit and resolve ambiguity up front rather than relying on implicit undefined propagation through chained conditionals:
```ts
// Bad: undefined tier falls through to the wrong branch
if (authParams?.tier === "free") {
  return 100;
}
return 10_000;

// Good: explicitly normalize the nullable value first
const tier = authParams?.tier ?? "free";
if (tier === "free") {
  return 100;
}
return 10_000;
```

Likewise, guard against nullable/empty collections before indexing into them, rather than assuming a value exists:
```ts
if (
  responseBody?.item?.content &&
  Array.isArray(responseBody.item.content) &&
  responseBody.item.content.length
) {
  const first = responseBody.item.content[0];
  // ...
}
```

In short: treat every `?.` and `??` as a decision point—decide deliberately whether to default, skip, log, or surface the missing value, rather than letting an implicit fallback hide bugs or alerting gaps.</description>
