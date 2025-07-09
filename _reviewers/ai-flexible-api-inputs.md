---
title: Flexible API inputs
description: Design APIs to accept flexible input formats and schema structures, ensuring
  a better developer experience while maintaining consistency in internal implementation.
repository: vercel/ai
label: API
language: Markdown
comments_count: 2
repository_stars: 15590
---

Design APIs to accept flexible input formats and schema structures, ensuring a better developer experience while maintaining consistency in internal implementation.

For input parameters, support multiple formats where reasonable:
```ts
// Instead of requiring only URL objects:
const { text } = await transcribe({
  model: revai.transcription('machine'),
  audio: new URL('https://example.com/audio.mp3'),
});

// Also support string URLs:
const { text } = await transcribe({
  model: revai.transcription('machine'),
  audio: 'https://example.com/audio.mp3',
});
```

For schema definitions, ensure support for flexible structures including additional properties where appropriate:
```ts
// Support additional properties in schemas
// e.g., using z.record(z.string()) or additionalProperties in JSON Schema
```

When implementing format flexibility:
- Use consistent conversion mechanisms across the entire API surface rather than creating one-off solutions
- Consider schema limitations of underlying services
- Document supported formats clearly in the API documentation
- Plan for compatibility across different components that may share schemas