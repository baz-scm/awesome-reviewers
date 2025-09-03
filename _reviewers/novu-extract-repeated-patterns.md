---
title: Extract repeated patterns
description: Extract repeated code patterns, CSS classes, and constants to improve
  maintainability and reduce duplication. When the same values, classes, or logic
  appear multiple times, consolidate them into reusable constants or utilities.
repository: novuhq/novu
label: Code Style
language: TSX
comments_count: 5
repository_stars: 37700
---

Extract repeated code patterns, CSS classes, and constants to improve maintainability and reduce duplication. When the same values, classes, or logic appear multiple times, consolidate them into reusable constants or utilities.

For CSS classes, extract repeated combinations into constants:
```typescript
// Instead of duplicating classes
const tabTriggerClasses = "relative text-xs font-medium text-[#525866] transition-colors hover:text-[#dd2476] data-[state=active]:text-[#dd2476]";

<TabsTrigger value="cli" className={tabTriggerClasses}>CLI</TabsTrigger>
<TabsTrigger value="manual" className={tabTriggerClasses}>Manual</TabsTrigger>
```

For animations and transitions, reuse predefined constants:
```typescript
// Use existing animation constants
import { fadeIn } from './animations';

<motion.div {...fadeIn} />
```

For callbacks and event handlers, define once and reuse:
```typescript
// Define callback once
const handleSave = () => saveForm();

// Reuse across multiple props
<QueryBuilder 
  onAddRule={handleSave}
  onUpdateRule={handleSave}
  onRemoveRule={handleSave}
/>
```

Use proper utility functions for className concatenation instead of string interpolation:
```typescript
// Use cn utility for proper class merging
className={cn('base-classes', conditionalClass && 'conditional-classes', className)}
```

This approach reduces maintenance burden, prevents inconsistencies, and makes the codebase more readable and reliable.