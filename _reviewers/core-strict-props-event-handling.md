---
title: Strict props event handling
description: 'Enforce strict typing and consistent handling of component props and
  events to ensure type safety, runtime validation, and maintainable component interfaces.
  Key guidelines:'
repository: vuejs/core
label: Vue
language: TypeScript
comments_count: 6
repository_stars: 50769
---

Enforce strict typing and consistent handling of component props and events to ensure type safety, runtime validation, and maintainable component interfaces. Key guidelines:

1. Always declare prop types explicitly with runtime validators:
```js
export default {
  props: {
    value: {
      type: Number,
      required: true,
      validator: (val) => val >= 0
    },
    options: {
      type: Array,
      default: () => [] // Use function for object/array defaults
    }
  }
}
```

2. Use typed emits declaration to enable proper type checking:
```js
export default {
  emits: {
    'update:modelValue': (value: number) => value >= 0,
    'change': (value: number, oldValue: number) => true
  }
}
```

3. Maintain consistent event naming:
- Use kebab-case for event names (e.g., 'item-selected')
- Prefix v-model events with 'update:'
- Document event payload types

4. Validate props access:
- Access props through defineProps in setup
- Avoid direct mutation of props
- Use computed properties for derived prop values

This ensures components are type-safe, self-documenting, and maintainable while preventing common runtime errors.