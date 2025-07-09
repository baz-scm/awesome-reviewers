---
title: Verify AI model capabilities
description: 'Always verify and accurately document AI model capabilities, supported
  formats, and limitations before implementation. Use consistent terminology (e.g.,
  "multi-modal" instead of "multimodal") and validate model features against official
  documentation sources. When documenting AI functionalities:'
repository: vercel/ai
label: AI
language: Other
comments_count: 6
repository_stars: 15590
---

Always verify and accurately document AI model capabilities, supported formats, and limitations before implementation. Use consistent terminology (e.g., "multi-modal" instead of "multimodal") and validate model features against official documentation sources. When documenting AI functionalities:

1. Be explicit about supported features and limitations
2. Link to official documentation when describing specific capabilities
3. Don't assume cross-functionality unless confirmed
4. Use clear, concise language when describing input formats and parameters

Example:
```typescript
// GOOD: Accurate, verified documentation with specific capabilities
// Groq's multi-modal models like `meta-llama/llama-4-scout-17b-16e-instruct` 
// support image inputs via URLs or base64-encoded data
// Source: https://groq.com/docs/models/llama-4-scout

// BAD: Unverified or inaccurate information
// OpenAI's o4 model is available (incorrect - only o4-mini is publicly available)
// Assuming a model supports certain parameter formats without verification
```

Maintaining accurate documentation saves development time, prevents integration errors, and helps teams properly utilize AI capabilities within their applications.