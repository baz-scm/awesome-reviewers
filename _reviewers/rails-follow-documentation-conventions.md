---
title: Follow documentation conventions
description: 'Maintain consistent formatting and style in all documentation to improve
  readability and professionalism:


  1. **Use proper formatting for code elements**:'
repository: rails/rails
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 57027
---

Maintain consistent formatting and style in all documentation to improve readability and professionalism:

1. **Use proper formatting for code elements**:
   - Wrap boolean values in backticks: `true`, `false` instead of true, false
   - Maintain prompt symbols (`$`) in command-line examples:
     ```bash
     $ rails new app_name
     ```

2. **Use correct Rails component names**:
   - Write "Active Record", not "ActiveRecord"
   - Write "Active Model", not "ActiveModel" 
   - Write "Action View", not "ActionView"

3. **Optimize cross-references**:
   - Add context links between related documentation sections:
     ```markdown
     See the [Getting Started Guide](getting_started.html#adding-authentication) for more details.
     ```
   - Link to sections within the same guide when possible to avoid navigating away
   - Use standard URL patterns: `api.rubyonrails.org` not `edgeapi.rubyonrails.org`

4. **Ensure example consistency**:
   - Make sure code examples match their accompanying explanatory text
   - When updating code or descriptions, ensure both remain in sync

Following these conventions creates a cohesive documentation experience that helps developers find information quickly and understand it correctly.
