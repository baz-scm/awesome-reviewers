---
title: AI provider naming standards
description: Maintain consistent and proper naming conventions for AI model providers
  throughout code, documentation, and comments. Use official capitalization (e.g.,
  "OpenAI" not "openai") and provide clear documentation about which AI services are
  required versus optional.
repository: browserbase/stagehand
label: AI
language: Markdown
comments_count: 2
repository_stars: 16443
---

Maintain consistent and proper naming conventions for AI model providers throughout code, documentation, and comments. Use official capitalization (e.g., "OpenAI" not "openai") and provide clear documentation about which AI services are required versus optional.

When documenting AI model requirements:
- Use proper capitalization for provider names (OpenAI, Anthropic, etc.)
- Clearly specify which providers are required vs optional
- Include setup instructions with correct environment variable names

Example:
```typescript
// Good: Proper capitalization and clear requirements
// Stagehand requires OpenAI as a model provider
const stagehand = new Stagehand({
  env: "LOCAL",
});

// Documentation should state:
// "NOTE: Stagehand client will default to OpenAI if these are not specified"
```

This ensures professional presentation, reduces confusion about service requirements, and maintains consistency across the codebase when referencing external AI providers.