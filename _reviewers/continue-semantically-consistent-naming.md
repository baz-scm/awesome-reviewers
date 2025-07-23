---
title: Semantically consistent naming
description: Names should accurately reflect their purpose and be used consistently
  throughout the codebase. This applies to props, function names, variables, and UI
  labels.
repository: continuedev/continue
label: Naming Conventions
language: TSX
comments_count: 6
repository_stars: 27819
---

Names should accurately reflect their purpose and be used consistently throughout the codebase. This applies to props, function names, variables, and UI labels.

1. **Maintain prop naming consistency**: When components share similar functionality, ensure prop names are consistent. If a component expects a specific prop structure, all implementations should use the same naming pattern.

```typescript
// Inconsistent - avoid this:
<EditFile changes={args.diff ?? ""} />
<EditFile changes={args.changes ?? ""} />

// Consistent - do this:
<EditFile changes={args.changes ?? ""} />
<EditFile changes={args.changes ?? ""} />
```

2. **Match UI labels to actions**: Ensure that button labels and UI text accurately reflect the actions they perform.

```typescript
// Misleading - avoid this:
<span onClick={() => void dispatch(cancelStream())}>Pause</span>

// Clear and accurate - do this:
<span onClick={() => void dispatch(cancelStream())}>Cancel</span>
```

3. **Use semantically clear prop names**: Choose prop names that clearly reflect their purpose. Avoid using event handler prefixes ('on-') for props that aren't event handlers.

```typescript
// Unclear semantics - avoid this:
<Switch onWarningText="This is a warning" />

// Clear semantics - do this:
<Switch warningText="This is a warning" />
```

4. **When renaming variables or props**: Ensure all references are updated throughout the codebase to maintain consistency and prevent runtime errors.

Following these guidelines helps prevent bugs, improves code readability, and makes the codebase more maintainable.