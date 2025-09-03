---
title: Use semantic descriptive names
description: Choose variable, function, and type names that clearly communicate their
  purpose, source, and context. Names should be self-documenting and avoid ambiguity
  or conflicts with existing identifiers.
repository: ant-design/ant-design
label: Naming Conventions
language: TSX
comments_count: 7
repository_stars: 95882
---

Choose variable, function, and type names that clearly communicate their purpose, source, and context. Names should be self-documenting and avoid ambiguity or conflicts with existing identifiers.

Key principles:
- Use specific, descriptive names over generic ones (e.g., `formItemName` instead of `defaultName`, `ButtonClassNamesType` instead of generic `Partial<Record<...>>`)
- Avoid naming conflicts by using distinct aliases when necessary (e.g., `cls` for classnames utility vs `classNames` for semantic props)
- Maintain consistency across similar components (e.g., use `iconPosition` consistently rather than mixing `iconPos` and `iconPosition`)
- Prefer names that don't require users to understand complex internal relationships

Example:
```typescript
// ❌ Generic and potentially confusing
const defaultName = useId();
classNames?: Partial<Record<ButtonSemanticName, string>>;

// ✅ Semantic and descriptive  
const randomId = useId();
const defaultName = formItemName || randomId;
classNames?: ButtonClassNamesType;

// ❌ Naming conflict
import classNames from 'classnames';
// ... later in code
<div classNames={props.classNames} />

// ✅ Clear distinction
import cls from 'classnames';
// ... later in code  
<div className={cls(...)} classNames={props.classNames} />
```