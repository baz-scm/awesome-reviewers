---
title: API parameter design
description: Design API methods with structured object parameters instead of ordered
  parameters or loose typing. Use proper TypeScript types rather than `any`, and consider
  parameter patterns that enhance safety and flexibility.
repository: browserbase/stagehand
label: API
language: TypeScript
comments_count: 4
repository_stars: 16443
---

Design API methods with structured object parameters instead of ordered parameters or loose typing. Use proper TypeScript types rather than `any`, and consider parameter patterns that enhance safety and flexibility.

Key principles:
- **Object parameters over ordered parameters**: Instead of `function(param1, param2, param3)`, use `function({ param1, param2, param3 })` for better readability and extensibility
- **Proper typing**: Replace `any` types with specific interfaces like `GotoOptions` to provide better developer experience and catch errors early
- **Safety through design**: Consider index-based parameters or other patterns that prevent edge cases, such as `context.pages()[index]` instead of direct page references
- **Support for templating**: Design APIs that can handle dynamic content through structured approaches like `{ action: "search for %query%", variables: { query: "value" } }`

Example transformation:
```typescript
// Before: Ordered parameters with loose typing
page.goto = async (url: string, options?: any) => { ... }

// After: Proper typing and structured approach
page.goto = async (url: string, options?: GotoOptions) => { ... }

// Before: Multiple ordered parameters
resolveLLMClient(llmClient, modelName, requestId)

// After: Object parameter with proper typing
resolveLLMClient({ 
  llmProvider, 
  modelName, 
  requestId 
}: { 
  llmClient?: LLMClient, 
  modelName?: AvailableModel, 
  requestId?: string 
})
```

This approach improves API discoverability, reduces parameter ordering mistakes, and makes future extensions easier without breaking existing code.