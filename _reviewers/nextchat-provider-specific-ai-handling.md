---
title: Provider-specific AI handling
description: Implement provider-specific logic when integrating different AI services,
  as each provider has unique requirements for message formatting, API endpoints,
  validation rules, and optimization strategies.
repository: ChatGPTNextWeb/NextChat
label: AI
language: TypeScript
comments_count: 6
repository_stars: 85721
---

Implement provider-specific logic when integrating different AI services, as each provider has unique requirements for message formatting, API endpoints, validation rules, and optimization strategies.

Different AI providers require distinct handling approaches:

**Message Role Handling**: Transform message roles based on provider requirements. For example, Baidu requires system messages to be converted to assistant/user roles and maintains strict alternating patterns, while Google converts system roles to user roles.

```typescript
// Provider-specific message role transformation
const messages = options.messages.map((v) => ({
  role: v.role === "system" ? "assistant" : v.role, // Baidu-specific
  content: getMessageTextContent(v),
}));

// vs Google-specific transformation
role: v.role.replace("assistant", "model").replace("system", "user"),
```

**API Path Construction**: Use provider-specific URL patterns and model handling. Azure requires deployment names in URLs, while Gemini needs dynamic model injection into paths.

```typescript
// Provider-specific path handling
if (modelConfig.providerName == ServiceProvider.Azure) {
  chatPath = this.path(`/deployments/${deploymentName}/chat/completions`);
} else {
  chatPath = this.path(OpenaiPath.ChatPath);
}
```

**Model-Specific Optimization**: Apply provider-specific models for different operations like summarization, using each provider's most suitable and cost-effective options rather than defaulting to a single model across all providers.

This approach ensures compatibility, optimal performance, and proper functionality across different AI service providers while maintaining clean, maintainable code.