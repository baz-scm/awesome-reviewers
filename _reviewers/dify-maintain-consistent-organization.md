---
title: Maintain consistent organization
description: Ensure proper file organization and consistent import conventions throughout
  the codebase. Assets should be placed in designated folders, utility functions should
  be moved to appropriate shared locations, and import paths should follow established
  patterns.
repository: langgenius/dify
label: Code Style
language: TSX
comments_count: 3
repository_stars: 114231
---

Ensure proper file organization and consistent import conventions throughout the codebase. Assets should be placed in designated folders, utility functions should be moved to appropriate shared locations, and import paths should follow established patterns.

Key practices:
- Move assets (images, fonts, etc.) to proper asset directories instead of keeping them in component folders
- Extract utility functions to shared locations like `utils/` directories rather than embedding them in component files
- Use consistent import path conventions (e.g., always use `@/app/` prefix for internal imports)
- Organize code by logical groupings and maintain clear separation of concerns

Example of proper organization:
```typescript
// Instead of: bg-[url('~@/app/components/tools/add-tool-modal/empty.png')]
// Use: bg-[url('/assets/empty.png')]

// Instead of: import useAvailableVarList from '../../_base/hooks/use-available-var-list'
// Use: import useAvailableVarList from '@/app/components/workflow/nodes/_base/hooks/use-available-var-list'

// Move utility functions from component files to shared locations:
// From: web/app/components/base/chat/embedded-chatbot/hooks.tsx
// To: web/app/components/base/chat/utils/index.ts
```

This approach improves code maintainability, makes dependencies clearer, and ensures consistent project structure across the team.