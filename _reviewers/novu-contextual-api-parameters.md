---
title: contextual API parameters
description: Design APIs to provide contextual information and adapt behavior based
  on current usage context. Pass context objects to callbacks, compute derived attributes
  based on state, and generate appropriate options dynamically.
repository: novuhq/novu
label: API
language: TSX
comments_count: 5
repository_stars: 37700
---

Design APIs to provide contextual information and adapt behavior based on current usage context. Pass context objects to callbacks, compute derived attributes based on state, and generate appropriate options dynamically.

When designing component APIs, include context parameters that provide relevant state information to callback functions. This enables more intelligent behavior and better integration.

Example:
```typescript
// Good: Provide context to callbacks
const notification = {
  context: { notification: props.notification } satisfies Parameters<AppearanceCallback['notification']>[0]
};

// Good: Compute derived attributes based on context
if (isEnhancedDigestEnabled && (isTextVariable || isUrlVariable)) {
  const aliasFor = resolveRepeatBlockAlias(
    isTextVariable ? (text ?? '') : (url ?? ''),
    editor,
    isEnhancedDigestEnabled
  );
  return commands.updateButton?.({ ...attrs, aliasFor: aliasFor ?? null });
}

// Good: Generate options based on variable context
const options = useMemo(() => {
  if (variableName.match(/^steps\..+\.events$/)) {
    return variables.filter((v) => v.name.startsWith('payload')).map((v) => ({ label: v.name, value: v.name }));
  }
  return [];
}, [variableName, variables]);
```

This approach makes APIs more intelligent and reduces the burden on API consumers to manually compute contextual information.