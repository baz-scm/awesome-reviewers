---
title: Prevent null reference exceptions
description: Always use optional chaining and nullish coalescing operators to prevent
  runtime errors when accessing properties or methods on potentially undefined objects.
repository: n8n-io/n8n
label: Null Handling
language: Other
comments_count: 8
repository_stars: 122978
---

Always use optional chaining and nullish coalescing operators to prevent runtime errors when accessing properties or methods on potentially undefined objects.

**Key practices:**

1. Use optional chaining (`?.`) when accessing properties that may be undefined:
   ```typescript
   // UNSAFE: May throw if connectionsByDestinationNode[name] is undefined
   const activeNodeConnections = 
     workflowsStore.connectionsByDestinationNode[activeNode.value.name].main || [];
   
   // SAFE: Uses optional chaining to prevent runtime errors
   const activeNodeConnections = 
     workflowsStore.connectionsByDestinationNode[activeNode.value.name]?.main || [];
   ```

2. Apply optional chaining at every level in property chains:
   ```typescript
   // UNSAFE: Only checks if node.value exists, but not if type exists
   const packageName = computed(() => node.value?.type.split('.')[0] ?? '');
   
   // SAFE: Checks both node.value and type before calling split
   const packageName = computed(() => node.value?.type?.split('.')[0] ?? '');
   ```

3. Choose appropriate default value operators:
   - Use `??` (nullish coalescing) when you only want to provide a default for `null` or `undefined`
   - Use `||` (logical OR) when you want to provide a default for any falsy value (empty string, 0, false)
   ```typescript
   // Only use a default when the value is null/undefined
   return (props.inputDataLength ?? 1) > 1;
   
   // Use a default for any falsy value, including empty strings
   :placement="tooltipPlacement || 'right'"
   ```

4. When dealing with deeply nested properties, ensure all levels are checked:
   ```typescript
   // UNSAFE: Will throw if node.value.parameters is undefined
   resource: node.value?.parameters.resource
   
   // SAFE: Checks both node.value and parameters before accessing resource
   resource: node.value?.parameters?.resource
   ```

This pattern makes your code more resilient by preventing the most common cause of runtime exceptions.