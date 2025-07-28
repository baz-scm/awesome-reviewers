---
title: Maintain documentation consistency
description: When modifying documentation structure or content, ensure all cross-references
  remain valid and avoid creating inconsistencies between related documents. Before
  renaming files or restructuring documentation, search for and update all internal
  links that reference the changed content. When platform-specific documentation exists
  alongside general guides,...
repository: logseq/logseq
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 37695
---

When modifying documentation structure or content, ensure all cross-references remain valid and avoid creating inconsistencies between related documents. Before renaming files or restructuring documentation, search for and update all internal links that reference the changed content. When platform-specific documentation exists alongside general guides, focus each document on its specific scope rather than duplicating information that could become out of sync.

For example, when updating a Windows-specific setup guide, reference the main development guide for common steps rather than duplicating them:

```markdown
# Build Logseq Desktop on Windows

This guide covers Windows-specific setup requirements. 
For general development instructions, see [develop-logseq.md](develop-logseq.md).

## Windows Pre-requisites
* Visual Studio (required for desktop app)
* Windows-specific Node.js setup via winget
```

Always include relevant cross-references to help developers find related documentation, and verify that structural changes don't break the documentation navigation flow.