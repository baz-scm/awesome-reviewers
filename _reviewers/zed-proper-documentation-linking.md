---
title: Proper documentation linking
description: 'Documentation should use appropriate linking strategies to ensure content
  remains accessible and navigable across all deployment environments:


  1. **Use absolute URLs for repository links**: When referencing files within the
  codebase (like READMEs or source files), always use absolute GitHub URLs instead
  of relative paths that may break when documentation...'
repository: zed-industries/zed
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 62119
---

Documentation should use appropriate linking strategies to ensure content remains accessible and navigable across all deployment environments:

1. **Use absolute URLs for repository links**: When referencing files within the codebase (like READMEs or source files), always use absolute GitHub URLs instead of relative paths that may break when documentation is deployed to external sites.

   ```markdown
   <!-- Incorrect -->
   Follow the steps in the [collab README](../../../crates/collab/README.md)

   <!-- Correct -->
   Follow the steps in the [collab README](https://github.com/organization/repo/blob/main/crates/collab/README.md)
   ```

2. **Implement cross-references between related documentation**: When functionality is documented across multiple locations, add cross-references to help users find all relevant information. This is particularly important for features that have both configuration and usage instructions in different sections.

3. **Test links in the deployed environment**: Verify that all documentation links work correctly not just in the source repository, but also in the final deployed documentation site.

Following these practices ensures documentation remains navigable and useful regardless of where or how users access it.