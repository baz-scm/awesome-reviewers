---
title: Vue component type safety
description: 'When defining Vue components with TypeScript, use appropriate component
  definition patterns to ensure proper type inference and avoid breaking type changes. '
repository: vuejs/core
label: Vue
language: TSX
comments_count: 3
repository_stars: 50769
---

When defining Vue components with TypeScript, use appropriate component definition patterns to ensure proper type inference and avoid breaking type changes. 

For proper typing of component props:

1. Use the correct helper for your component definition needs. For example, `DeclareComponent` may be more appropriate than `defineComponent` when you need to expose prop types in a specific way.

2. When providing default values for function props, remember they're handled differently than object/array defaults:

```ts
// Correct way to define function props with defaults
props: {
  handler: {
    type: Function,
    // Function props don't need to be wrapped in factory functions
    default() {
      return (value) => console.log(value)
    }
  },
  // While object defaults need factory functions
  objProp: {
    type: Object,
    default: () => ({ key: 'value' })
  }
}
```

3. Be cautious when modifying type definitions or signatures of public APIs, as these can introduce breaking changes for consumers. Maintain the expected type argument order for exported types like `DefineComponent`.

By following these practices, you'll ensure your Vue components have proper TypeScript support while maintaining compatibility with Vue's type system.