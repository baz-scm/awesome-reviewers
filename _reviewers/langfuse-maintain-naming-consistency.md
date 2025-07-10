---
title: Maintain naming consistency
description: 'Use consistent and descriptive names for variables, components, and
  functions throughout the codebase. When the same concept appears in multiple places,
  use identical naming to prevent confusion and bugs. This includes:'
repository: langfuse/langfuse
label: Naming Conventions
language: TSX
comments_count: 6
repository_stars: 13574
---

Use consistent and descriptive names for variables, components, and functions throughout the codebase. When the same concept appears in multiple places, use identical naming to prevent confusion and bugs. This includes:

1. **Consistent variable names within functions**: If you name a variable in one way at the start of a function, use the same name throughout.

```typescript
// Inconsistent (confusing):
const modelToProviderMap = useMemo(() => {
  const modelProviderMap: Record<string, string> = {}; // Different name!
  // ...
}, [apiKeys.data]);

// Consistent (clear):
const modelToProviderMap = useMemo(() => {
  const modelToProviderMap: Record<string, string> = {}; // Same name
  // ...
}, [apiKeys.data]);
```

2. **Component names that reflect functionality**: When a component's purpose changes, rename it to match its current behavior.

```typescript
// Misleading (no longer a dropdown):
export function DownloadDropdown({ /* ... */ }) {
  // Renders a single button, not a dropdown
}

// Clear (matches functionality):
export function DownloadButton({ /* ... */ }) {
  // Renders a single button
}
```

3. **Boolean variables with 'is' prefix**: Use the 'is' prefix for boolean variables to improve readability.

```typescript
// Less clear:
const autoLocked = useState<boolean>(isExistingWidget);

// More clear:
const isAutoLocked = useState<boolean>(isExistingWidget);
```

4. **Consistent property names**: Use the same property names across related components.

```typescript
// Inconsistent:
totalTokens: props.observations.map(/* ... */)

// Consistent with other code:
totalUsage: props.observations.map(/* ... */)
```

5. **Avoid typos in identifiers**: Ensure component and variable names are spelled correctly.

```typescript
// Incorrect:
export const PeakViewTraceDetail = ({ projectId }: { projectId: string }) => {

// Correct (matches file path and context):
export const PeekViewTraceDetail = ({ projectId }: { projectId: string }) => {
```

Consistent naming reduces cognitive load for developers, makes the codebase more maintainable, and helps prevent bugs caused by name confusion.