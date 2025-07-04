---
title: Consistent term capitalization
description: 'Follow consistent capitalization rules for technical terms, acronyms,
  and library names throughout your codebase and documentation:


  1. **Capitalize standard acronyms**: Use ''URL'', ''JSON'', ''API'', ''HTML'', ''CSS'',
  ''Unicode'', etc. rather than lowercase versions.'
repository: pydantic/pydantic
label: Naming Conventions
language: Markdown
comments_count: 7
repository_stars: 24377
---

Follow consistent capitalization rules for technical terms, acronyms, and library names throughout your codebase and documentation:

1. **Capitalize standard acronyms**: Use 'URL', 'JSON', 'API', 'HTML', 'CSS', 'Unicode', etc. rather than lowercase versions.

2. **Capitalize product/library names**: Use 'Pydantic', 'Django', 'React', etc. when referring to them as proper nouns in documentation, comments, and string literals.

3. **Preserve lowercase in code contexts**: Keep technical names lowercase when used in import statements, function calls, or paths where they must match the actual implementation:
   ```python
   # Correct:
   import pydantic  # lowercase in import statements
   
   # In documentation or comments:
   # Pydantic provides validation for Python data types  # capitalized as proper noun
   ```

This consistency enhances readability, maintains technical accuracy, and provides a more professional appearance in your documentation and user-facing messages.