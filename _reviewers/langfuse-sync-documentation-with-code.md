---
title: Sync documentation with code
description: 'Always ensure documentation and comments accurately reflect the actual
  code implementation. When modifying code, update all related documentation to maintain
  consistency. This applies to:'
repository: langfuse/langfuse
label: Documentation
language: TypeScript
comments_count: 9
repository_stars: 13574
---

Always ensure documentation and comments accurately reflect the actual code implementation. When modifying code, update all related documentation to maintain consistency. This applies to:

1. **Function behavior descriptions**: Make sure JSDoc comments and inline comments accurately describe what functions do.
   ```typescript
   /**
    * Creates a table view preset // Not "Creates a saved view"
    */
   ```

2. **Parameter types**: Ensure type annotations in documentation match the actual types used in code.
   ```typescript
   /**
    * @param {string} projectId - Project ID for the observation // Not {Object}
    */
   ```

3. **Constants and threshold values**: Document the actual values used in conditions.
   ```typescript
   /**
    * Specialized formatter for very small numbers (10^-3 to 10^-15 range) // Not 10^-6 if code uses 10^-3
    */
   
   // If no fromStartTime or startTime is provided, use a 1-day lookback for a faster query // Be specific
   ```

4. **Time-related values**: When changing durations or time-based configurations, update the corresponding documentation.
   ```typescript
   // Process at most `max` jobs per 120 seconds // Not "30 seconds" if the value is 120_000
   ```

Accurate documentation reduces confusion, speeds up onboarding for new team members, and prevents bugs caused by misunderstanding code behavior. Review all documentation changes as carefully as you review code changes.