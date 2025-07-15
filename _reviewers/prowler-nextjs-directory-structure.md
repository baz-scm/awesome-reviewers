---
title: Next.js directory structure
description: Keep the Next.js `/app` directory strictly for routing purposes as per
  framework conventions. Non-routing related code like tools, utilities, and services
  should be moved to appropriate directories such as `/lib/`. This improves code organization,
  maintainability, and follows Next.js best practices.
repository: prowler-cloud/prowler
label: Code Style
language: TypeScript
comments_count: 10
repository_stars: 11834
---

Keep the Next.js `/app` directory strictly for routing purposes as per framework conventions. Non-routing related code like tools, utilities, and services should be moved to appropriate directories such as `/lib/`. This improves code organization, maintainability, and follows Next.js best practices.

For example, instead of:
```typescript
// ui/app/(ai)/analyst/(tools)/checks.ts
import { tool } from "@langchain/core/tools";
import { aiGetProviderChecks } from "@/lib/lighthouse/helperChecks";
import { checkSchema } from "@/types/ai/checks";

export const getProviderChecksTool = tool(
  // tool implementation
);
```

Use:
```typescript
// ui/lib/lighthouse/tools/checks.ts
import { tool } from "@langchain/core/tools";
import { aiGetProviderChecks } from "@/lib/lighthouse/helperChecks";
import { checkSchema } from "@/types/ai/checks";

export const getProviderChecksTool = tool(
  // tool implementation
);
```

This organization makes the codebase more maintainable and follows the intended use of the Next.js app directory structure.