---
title: Component naming consistency
description: Ensure component usage in templates matches registered components. Vue
  components must be referenced in templates by either their kebab-case equivalent
  or by their exact registered name.
repository: n8n-io/n8n
label: Vue
language: TypeScript
comments_count: 12
repository_stars: 122978
---

Ensure component usage in templates matches registered components. Vue components must be referenced in templates by either their kebab-case equivalent or by their exact registered name.

When registering a component:
```js
components: {
  N8nIcon,
},
```

Use it in templates with the matching kebab-case name:
```html
<n8n-icon v-bind="args" />
```

Or with the exact registered name:
```html
<N8nIcon v-bind="args" />
```

Using inconsistent names like `<flowstate-icon>` when the component is registered as `N8nIcon` will cause runtime errors because Vue will not recognize the element.

This also applies to all component closing tags, which should match the opening tag. Consistent component naming helps prevent runtime errors, improves code readability, and follows Vue's standard conventions.