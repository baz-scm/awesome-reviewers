---
title: Test before documenting
description: 'Always thoroughly test API features and endpoints before documenting
  them, especially when integrating with third-party services. Documentation should
  accurately reflect the actual behavior of the API, including:'
repository: vercel/ai
label: API
language: Other
comments_count: 3
repository_stars: 15590
---

Always thoroughly test API features and endpoints before documenting them, especially when integrating with third-party services. Documentation should accurately reflect the actual behavior of the API, including:

- Precise error descriptions that explain causes and resolutions
- Clear indication of limitations or inconsistencies across different providers
- Executable code examples that users can adapt to their needs

For error documentation, focus on specific causes rather than general descriptions:

```ts
// DON'T: Use vague descriptions
// "APICallError occurs when there's an issue during an API call"

// DO: Be specific about error causes
// "APICallError occurs when a provider API returns an error response,
// typically due to invalid message structure. Always check the provider's
// error message for specific resolution steps."
```

For third-party integrations, test thoroughly and document any limitations:

```ts
// Example: Adding appropriate warnings for feature limitations
if (isGoogleProvider && options.includeThoughts) {
  console.warn('includeThoughts is not fully supported in all Google Generative AI models.');
}
```

For code examples, ensure they are practical and executable:

```ts
// DON'T: Use abstract placeholders without explanation
const { transcript } = await generateTranscript({
  model: openai.transcription('whisper-1'),
  audio: audioData, // What is audioData?
});

// DO: Provide complete, executable examples
import fs from 'fs/promises';

const audioData = await fs.readFile('./sample-audio.mp3');
const { transcript } = await generateTranscript({
  model: openai.transcription('whisper-1'),
  audio: audioData,
});
```

This standard ensures that developers can rely on your documentation to accurately understand how to use your API properly, reducing confusion and support issues.