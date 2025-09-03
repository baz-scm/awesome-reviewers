---
title: leverage existing solutions
description: Avoid duplicating functionality by leveraging existing libraries and
  creating reusable components. Instead of redefining common utilities or creating
  similar components for each use case, use established libraries and build generic,
  reusable components that can be configured for different scenarios.
repository: menloresearch/jan
label: Code Style
language: TSX
comments_count: 2
repository_stars: 37620
---

Avoid duplicating functionality by leveraging existing libraries and creating reusable components. Instead of redefining common utilities or creating similar components for each use case, use established libraries and build generic, reusable components that can be configured for different scenarios.

For example, rather than redefining a classNames utility:
```typescript
// Avoid
function classNames(...classes: any) {
  // custom implementation
}

// Prefer
import classnames from 'classnames'
```

Similarly, create reusable components instead of duplicating similar functionality:
```typescript
// Instead of separate DeleteModal, ConfirmModal, etc.
// Create one ConfirmationModal that accepts different props
const ConfirmationModal: React.FC<Props> = ({ 
  atom, title, description, onConfirm 
}) => {
  // Generic modal implementation
}
```

This approach reduces code duplication, improves maintainability, and ensures consistency across the codebase.