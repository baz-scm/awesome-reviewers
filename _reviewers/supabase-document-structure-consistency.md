---
title: Document structure consistency
description: 'Maintain consistent document structure and formatting in documentation
  to improve readability and user experience. Follow these key principles:


  1. **Use sentence case for headings** - Only capitalize the first word and proper
  nouns:'
repository: supabase/supabase
label: Documentation
language: Other
comments_count: 7
repository_stars: 86070
---

Maintain consistent document structure and formatting in documentation to improve readability and user experience. Follow these key principles:

1. **Use sentence case for headings** - Only capitalize the first word and proper nouns:
   - ✅ "Rate limits" instead of "Rate Limits"
   - ✅ "Auth OTP/Magic link request limit" instead of "Auth OTP/Magic Link request limit"

2. **Follow proper heading hierarchy** - Avoid duplicate H1 headings when frontmatter already defines a title. Start content with H2:
   ```md
   ---
   title: 'Replication and Analytics with Supabase'
   ---
   
   ## Introduction
   Start your content here...
   
   ## Features
   ```

3. **Organize content logically** - Use clear section names and consider breaking long documents into focused pages:
   ```md
   ## Quickstart guide
   <!-- Keep this focused on getting started quickly -->
   
   ## Advanced development tips
   <!-- Move detailed tips to separate sections -->
   ```

4. **Use standardized admonition types** - Stick to approved types: `note`, `tip`, `caution`, `deprecation`, `danger`:
   ```md
   <Admonition type="caution" title="Be aware of changes">
     Highlight important information or warnings using appropriate admonition types
   </Admonition>
   ```

5. **Present step-by-step instructions clearly** - Structure multi-step processes with clear ordering and grouping:
   ```md
   ## Configuration
   
   ### Step 1: Set up credentials
   1. First do this...
   2. Then do that...
   
   ### Step 2: Configure settings
   ```

Following these standards ensures documentation remains consistent, accessible, and professional across the project.