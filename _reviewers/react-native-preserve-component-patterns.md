---
title: preserve component patterns
description: When refactoring React components, maintain essential component patterns
  including type annotations, ref forwarding capabilities, and thoughtful component
  composition. Avoid losing important functionality during simplification.
repository: facebook/react-native
label: React
language: JavaScript
comments_count: 4
repository_stars: 123178
---

When refactoring React components, maintain essential component patterns including type annotations, ref forwarding capabilities, and thoughtful component composition. Avoid losing important functionality during simplification.

Key considerations:
- Preserve component type annotations when converting between component patterns (e.g., forwardRef to regular functions)
- Ensure ref forwarding remains functional for parent components that need to pass refs
- Consider component hierarchy and whether wrapper components can be simplified or consolidated
- Maintain consistency with similar components in the codebase

Example of preserving component type during refactoring:
```javascript
// Before: forwardRef with component type
const View: component(...) = React.forwardRef(...)

// After: regular function but preserve the type
function View({...}: Props): React.Node {
  // component logic
}

export default View as component(
  ref?: React.RefSetter<React.ElementRef<typeof ViewNativeComponent>>,
  ...props: ViewProps
);
```

For ref forwarding, ensure parent components can still pass refs by merging internal refs with forwarded ones, similar to patterns used in TouchableOpacity. When restructuring component hierarchies (like SafeAreaView/View combinations), evaluate whether the nesting serves a purpose or can be simplified while maintaining the same functionality.