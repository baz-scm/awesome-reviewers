---
title: Document intent clearly
description: 'Add clear documentation that explains not just what code does, but why
  certain approaches were chosen. This applies to:


  1. **Complex code sections**: Add explanatory comments to complex logic, particularly
  SQL queries'
repository: supabase/supabase
label: Documentation
language: TSX
comments_count: 4
repository_stars: 86070
---

Add clear documentation that explains not just what code does, but why certain approaches were chosen. This applies to:

1. **Complex code sections**: Add explanatory comments to complex logic, particularly SQL queries
   ```sql
   -- last-used-api-keys: retrieves timestamp of most recent API key usage by role
   SELECT unix_millis(max(timestamp)) as timestamp, payload.role, payload.signature_prefix 
   FROM edge_logs cross join unnest(metadata) as m 
   -- additional joins...
   ```

2. **Implementation decisions**: Document the reasoning behind specific coding patterns
   ```javascript
   // Create a shallow copy to prevent unintended mutations to the original object
   custom_properties: 'properties' in event ? event.properties : {},
   ```
   
3. **UI elements**: Include tooltips for interactive elements to clarify their purpose
   
4. **Technical limitations**: Explicitly state constraints in user-facing documentation (e.g., "disk size can only be expanded, not shrunk")

Well-documented code improves maintainability, reduces onboarding time for new developers, and prevents misunderstandings about system behavior.