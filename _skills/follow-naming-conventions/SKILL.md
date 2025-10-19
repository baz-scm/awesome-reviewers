---
name: follow-naming-conventions
description: 'Use proper naming conventions to make code more readable and maintainable:
  1. **Functions should start with verbs** that describe their action: ```typescript'
version: '1.0'
---
# Follow naming conventions

Use proper naming conventions to make code more readable and maintainable:

1. **Functions should start with verbs** that describe their action:
   ```typescript
   // Incorrect
   const hasChanges = () => { ... }
   
   // Correct
   const checkForChanges = () => { ... }
   ```

2. **Use descriptive names for generated outputs** that include relevant context:
   ```typescript
   // Too generic
   element.download = `taskInstanceLogs.txt`;
   
   // Better - includes relevant identifiers
   element.download = `${dagId}-${taskId}-${runId}-${mapIndex}-${tryNumber}.txt`;
   ```

3. **Maintain consistent casing** for related identifiers, especially when filtering or comparing:
   ```typescript
   // Define consistent casing pattern for categories
   const existingCategories = ["user", "docs", "admin", "browse"];
   
   // Use consistent transformation when comparing
   if (!existingCategories.includes(category.toLowerCase())) {
     // ...
   }
   ```

Following these conventions improves code clarity and reduces confusion when maintaining code across a team.
