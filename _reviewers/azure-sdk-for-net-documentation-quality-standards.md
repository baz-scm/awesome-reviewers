---
title: Documentation quality standards
description: 'Ensure documentation is specific, complete, and actionable for developers:


  1. **Provide meaningful content** - Avoid vague descriptions like "Test changes"
  in changelogs. Instead, be specific about what was modified or tested:'
repository: Azure/azure-sdk-for-net
label: Documentation
language: Markdown
comments_count: 9
repository_stars: 5809
---

Ensure documentation is specific, complete, and actionable for developers:

1. **Provide meaningful content** - Avoid vague descriptions like "Test changes" in changelogs. Instead, be specific about what was modified or tested:
   ```diff
   - Test changes
   + Conducted internal testing to validate the integration of new features and ensure stability.
   ```

2. **Include context and references** - When mentioning external documentation or specifications, include properly formatted links to those resources. This makes it easier for developers to find related information:
   ```markdown
   `ManagedIdentityCredential` now retries 410 status responses as required by 
   [Azure IMDS documentation](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token).
   ```

3. **Ensure code examples are valid** - All code examples in documentation should be derived from compiled, tested code snippets to ensure they work correctly and remain valid over time.

4. **Add explanatory comments** - Include comments that explain the purpose of code transformations or complex configurations to help future maintainers understand why certain decisions were made:
   ```
   # This transform removes the `x-nullable` annotation to ensure compatibility 
   # with the generated SDK code, which does not support nullable collections.
   ```

5. **Remove redundancy** - Keep documentation concise by eliminating redundant explanations while maintaining clarity.

For changelogs specifically:
- Only mark changes as "breaking" between stable releases, not for beta versions
- Include specific details rather than placeholder headings
- Remove empty sections when there are no relevant changes
