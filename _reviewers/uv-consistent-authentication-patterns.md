---
title: Consistent authentication patterns
description: 'Design API authentication mechanisms with consistent patterns, clear
  documentation, and helpful error messages. When implementing authentication:


  1. **Document authentication requirements explicitly**:'
repository: astral-sh/uv
label: API
language: Markdown
comments_count: 4
repository_stars: 60322
---

Design API authentication mechanisms with consistent patterns, clear documentation, and helpful error messages. When implementing authentication:

1. **Document authentication requirements explicitly**:
   - Specify expected username/token formats and any special cases
   - Explain how authentication failures are handled

2. **Design credentials lookup intelligently**:
   ```python
   # Prefer using the base index URL for credential lookup
   # Instead of:
   credentials = keyring.get_credential(package_url, None)
   
   # Use:
   credentials = keyring.get_credential(index_url, None)
   ```

3. **Provide clear error messages for authentication failures**:
   ```
   If you use `--token "$JFROG_TOKEN"` with JFrog, you will receive a 
   401 Unauthorized error as JFrog requires an empty username but 
   uv passes `__token__` as the username when `--token` is used.
   ```

4. **Consider consistency across similar operations**:
   - Use the same authentication patterns for related endpoints
   - Document when different operations require different authentication formats
   - Be explicit about URL formatting requirements (e.g., trailing slashes)

5. **Test authentication edge cases**:
   - Verify behavior with missing credentials
   - Test various token formats
   - Confirm proper handling of authentication failures