---
title: Clear consistent identifier names
description: 'Choose clear, consistent, and non-redundant names for identifiers across
  the codebase. Follow these guidelines:


  1. Use specific, descriptive names that clearly indicate purpose:'
repository: neondatabase/neon
label: Naming Conventions
language: Rust
comments_count: 7
repository_stars: 19015
---

Choose clear, consistent, and non-redundant names for identifiers across the codebase. Follow these guidelines:

1. Use specific, descriptive names that clearly indicate purpose:
   ```rust
   // Bad
   type SegmentSize = u32;
   
   // Good
   type WalSegmentSize = u32;  // Clearly indicates this is for WAL segments
   ```

2. Maintain consistent naming patterns throughout the codebase:
   ```rust
   // Bad: Mixing naming patterns
   struct PostHogLocalEvaluationFlag {}
   struct LocalEvaluationResponse {}
   
   // Good: Consistent naming
   struct LocalEvaluationFlag {}
   struct LocalEvaluationResponse {}
   ```

3. Avoid redundant prefixes when context is clear:
   ```rust
   // Bad: Redundant context
   pub http_client: reqwest::Client  // In HTTP-specific module
   
   // Good: Clean, contextual naming
   pub client: reqwest::Client
   ```

4. Use clear, specific variable names in method parameters:
   ```rust
   // Bad: Ambiguous naming
   async fn from_request_parts(_: &mut Parts, state: &Arc<ComputeNode>)
   
   // Good: Clear purpose
   async fn from_request_parts(_: &mut Parts, compute: &Arc<ComputeNode>)
   ```

This standard helps maintain code readability and reduces confusion during code review and maintenance.