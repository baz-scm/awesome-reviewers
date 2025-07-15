---
title: Consistent provider options
description: When designing APIs that support multiple providers or service integrations,
  implement consistent patterns for handling provider-specific options. This includes
  proper validation, separation of request vs. non-request options, and clear type
  definitions.
repository: vercel/ai
label: API
language: TypeScript
comments_count: 5
repository_stars: 15590
---

When designing APIs that support multiple providers or service integrations, implement consistent patterns for handling provider-specific options. This includes proper validation, separation of request vs. non-request options, and clear type definitions.

Key practices:
1. Use schema validation for provider options before sending requests
2. Extract non-request options that shouldn't be sent to external APIs
3. Maintain consistent naming patterns across providers
4. Provide comprehensive type definitions with JSDoc comments

```typescript
// Good practice: Extract non-request options before API calls
const { pollIntervalMillis, maxPollAttempts, ...providerRequestOptions } = 
  providerOptions.luma ?? {};
  
// Good practice: Use standardized validation
const openaiOptions = parseProviderOptions({
  provider: 'openai',
  providerOptions,
  schema: openaiProviderOptionsSchema,
});

// Good practice: Well-documented provider option types
export type GladiaTranscriptionInitiateAPITypes = {
  /** URL to a Gladia file or to an external audio or video file */
  audio_url: string;
  /** [Alpha] Context to feed the transcription model with for better accuracy */
  context_prompt?: string;
  // Additional well-documented parameters...
};
```

This approach ensures type safety, prevents sending unnecessary options to external APIs, and makes your code more maintainable as you add support for new providers or update existing integrations.